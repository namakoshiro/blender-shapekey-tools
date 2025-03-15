import bpy
import os
import zipfile
import tempfile
import shutil
import sys
import time
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty
from bpy.types import Operator


def log(msg):
    # Print log message with prefix
    print(f"[Install] {msg}")

class SHAPEKEY_OT_update_from_local(Operator, ImportHelper):
    bl_idname = "shapekey.update_from_local"
    bl_label = "Install"
    bl_description = "Select a local zip file to update the addon"
    
    filename_ext = ".zip"
    filter_glob: StringProperty(default="*.zip", options={'HIDDEN'})
    
    def execute(self, context):
        log("Validating update package")
        zip_path = self.filepath
        if not os.path.exists(zip_path):
            log("Error: File not found")
            self.report({'ERROR'}, "File not found")
            return {'CANCELLED'}
        
        log("Extracting update package")
        # Get addon directory and name
        addon_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        addon_name = os.path.basename(addon_dir)
        
        # Store modules with register function
        main_modules = {}
        for mod_name in sys.modules.keys():
            if addon_name in mod_name and hasattr(sys.modules[mod_name], 'register'):
                main_modules[mod_name] = sys.modules[mod_name]
        
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                log("Extracting zip file")
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                
                # Find source directory
                source_dir = None
                for root, dirs, files in os.walk(temp_dir):
                    for dir_name in dirs:
                        if dir_name == addon_name or dir_name.startswith(addon_name + "-"):
                            source_dir = os.path.join(root, dir_name)
                            break
                    if source_dir:
                        break
                
                # If no matching directory found, look for __init__.py
                if not source_dir:
                    for root, dirs, files in os.walk(temp_dir):
                        if "__init__.py" in files:
                            source_dir = root
                            break
                
                if not source_dir:
                    log("Error: Could not find addon directory in zip file")
                    self.report({'ERROR'}, "Could not find addon directory in zip file")
                    return {'CANCELLED'}
                
                log(f"Found source directory: {source_dir}")
                
                # Backup current addon
                backup_dir = os.path.join(tempfile.gettempdir(), f"{addon_name}_backup_{int(time.time())}")
                log(f"Creating backup at {backup_dir}")
                shutil.copytree(addon_dir, backup_dir)
                
                # Remove current addon files (except .git directory)
                for item in os.listdir(addon_dir):
                    item_path = os.path.join(addon_dir, item)
                    if item != ".git" and os.path.exists(item_path):
                        if os.path.isdir(item_path):
                            shutil.rmtree(item_path)
                        else:
                            os.remove(item_path)
                
                # Copy new files
                for item in os.listdir(source_dir):
                    source_item = os.path.join(source_dir, item)
                    dest_item = os.path.join(addon_dir, item)
                    
                    if os.path.isdir(source_item):
                        shutil.copytree(source_item, dest_item)
                    else:
                        shutil.copy2(source_item, dest_item)
                
                log("Update installed successfully")
                
                # Refresh UI
                log("Refreshing UI")
                
                # Find the addon module in sys.modules
                addon_module = None
                for mod_name in list(sys.modules.keys()):
                    if mod_name == addon_name or mod_name.startswith(addon_name + "."):
                        if mod_name == addon_name:
                            addon_module = mod_name
                        del sys.modules[mod_name]
                
                # Try to re-enable the addon
                if addon_module:
                    log(f"Re-enabling addon module: {addon_module}")
                    force_enable_addon(addon_module)
                
                # Show success message
                self.report({'INFO'}, "Update installed successfully. Please restart Blender.")
                
                # Force redraw all areas
                def force_redraw_all():
                    for window in bpy.context.window_manager.windows:
                        for area in window.screen.areas:
                            area.tag_redraw()
                
                # Schedule redraw for next frame
                bpy.app.timers.register(force_redraw_all, first_interval=0.1)
                
                return {'FINISHED'}
                
            except Exception as e:
                log(f"Error installing update: {e}")
                
                # Restore from backup
                try:
                    log("Restoring from backup")
                    
                    # Remove current addon files
                    for item in os.listdir(addon_dir):
                        item_path = os.path.join(addon_dir, item)
                        if item != ".git" and os.path.exists(item_path):
                            if os.path.isdir(item_path):
                                shutil.rmtree(item_path)
                            else:
                                os.remove(item_path)
                    
                    # Copy backup files
                    for item in os.listdir(backup_dir):
                        backup_item = os.path.join(backup_dir, item)
                        dest_item = os.path.join(addon_dir, item)
                        
                        if os.path.isdir(backup_item):
                            shutil.copytree(backup_item, dest_item)
                        else:
                            shutil.copy2(backup_item, dest_item)
                    
                    log("Restored from backup")
                    self.report({'ERROR'}, f"Error installing update: {e}. Restored from backup.")
                    
                except Exception as restore_error:
                    log(f"Error restoring from backup: {restore_error}")
                    self.report({'ERROR'}, f"Critical error: {e}. Backup restoration failed: {restore_error}")
                
                return {'CANCELLED'}

def force_enable_addon(addon_module):
    # Re-enable addon and redraw UI
    try:
        bpy.ops.preferences.addon_enable(module=addon_module)
        
        # Force redraw all areas
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                area.tag_redraw()
                
        return True
    except Exception as e:
        log(f"Error enabling addon: {e}")
        return False

def register():
    bpy.utils.register_class(SHAPEKEY_OT_update_from_local)

def unregister():
    bpy.utils.unregister_class(SHAPEKEY_OT_update_from_local) 