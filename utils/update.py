import bpy
import os
import json
import re
import zipfile
import tempfile
import shutil
import sys
import time
import datetime
from bpy.props import StringProperty, BoolProperty
from bpy.types import Operator
import urllib.request
import urllib.error
import threading

def log(msg):
    # Print log message with prefix
    print(f"[Update] {msg}")

_latest_tag_name = ""

GITHUB_API_URL = "https://api.github.com/repos/namakoshiro/blender-shapekey-tools/releases/latest"

class SHAPEKEY_OT_update_from_online(Operator):
    bl_idname = "shapekey.update_from_online"
    bl_label = "Update"
    bl_description = "Check and download updates from GitHub"
    
    def get_current_version(self):
        # Read version from __init__.py
        addon_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        init_file = os.path.join(addon_dir, "__init__.py")
        with open(init_file, 'r') as f:
            content = f.read()
        version_match = re.search(r'"version":\s*\((\d+),\s*(\d+),\s*(\d+)\)', content)
        if version_match:
            return (int(version_match.group(1)), int(version_match.group(2)), int(version_match.group(3)))
        return None
    
    def get_latest_version_api(self):
        # Get latest version from GitHub API
        api_url = GITHUB_API_URL
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'Mozilla/5.0'
        }
        req = urllib.request.Request(api_url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode('utf-8'))
                tag_name = data.get('tag_name', '')
                
                # Extract version from tag name (e.g., "v1.2.3" -> (1,2,3))
                version_match = re.search(r'v?(\d+)\.(\d+)\.(\d+)', tag_name)
                if version_match:
                    return (int(version_match.group(1)), int(version_match.group(2)), int(version_match.group(3))), tag_name
        except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError) as e:
            log(f"Error checking for updates: {e}")
        return None, None
    
    def execute(self, context):
        global _latest_tag_name
        
        self.report({'INFO'}, "Checking for updates...")
        log("Getting current version")
        current_version = self.get_current_version()
        if not current_version:
            log("Error: Could not determine current version")
            self.report({'ERROR'}, "Could not determine current version")
            return {'CANCELLED'}
        log(f"Current version: {current_version[0]}.{current_version[1]}.{current_version[2]}")
        
        log("Retrieving latest version")
        latest_version, tag_name = self.get_latest_version_api()
        if not latest_version:
            log("Error: Could not retrieve latest version")
            self.report({'ERROR'}, "Could not retrieve latest version")
            return {'CANCELLED'}
        version_str = f"{latest_version[0]}.{latest_version[1]}.{latest_version[2]}"
        log(f"Latest version: {version_str}")
        
        _latest_tag_name = tag_name
        
        log("Comparing versions")
        # Check if update is needed
        is_newer = False
        if latest_version[0] > current_version[0]:
            is_newer = True
        elif latest_version[0] == current_version[0] and latest_version[1] > current_version[1]:
            is_newer = True
        elif latest_version[0] == current_version[0] and latest_version[1] == current_version[1] and latest_version[2] > current_version[2]:
            is_newer = True
        if not is_newer:
            log("No update required. Current version is up-to-date.")
            self.report({'INFO'}, f"You already have the latest version ({current_version[0]}.{current_version[1]}.{current_version[2]}) installed")
            return {'FINISHED'}
        
        log(f"Update available from {current_version[0]}.{current_version[1]}.{current_version[2]} to {version_str}")
        
        # Store version info in window manager
        context.window_manager["update_new_version"] = version_str
        context.window_manager["update_current_version"] = f"{current_version[0]}.{current_version[1]}.{current_version[2]}"
        
        bpy.ops.shapekey.show_update_dialog('INVOKE_DEFAULT')
        
        return {'FINISHED'}

class SHAPEKEY_OT_show_update_dialog(Operator):
    bl_idname = "shapekey.show_update_dialog"
    bl_label = "Update Available"
    bl_description = "Show update confirmation dialog"
    bl_options = {'REGISTER', 'INTERNAL'}
    
    def invoke(self, context, event):
        # Show dialog
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=200)
    
    def draw(self, context):
        # Draw dialog content
        layout = self.layout
        wm = context.window_manager
        
        new_version = wm.get("update_new_version", "unknown")
        current_version = wm.get("update_current_version", "unknown")
        
        layout.label(text=f"New version {new_version} is available!")
        layout.label(text=f"Current version: {current_version}")
        layout.label(text="Do you want to update?")
    
    def execute(self, context):
        # Confirm update
        bpy.ops.shapekey.confirm_update()
        return {'FINISHED'}
    
    def cancel(self, context):
        # Cancel update
        bpy.ops.shapekey.cancel_update()
        return {'CANCELLED'}

class SHAPEKEY_OT_confirm_update(Operator):
    bl_idname = "shapekey.confirm_update"
    bl_label = "Confirm Update"
    bl_description = "Confirm and download the update"
    
    def execute(self, context):
        log("Starting update process")
        
        # Get download URL from GitHub API
        api_url = GITHUB_API_URL
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'Mozilla/5.0'
        }
        req = urllib.request.Request(api_url, headers=headers)
        
        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode('utf-8'))
                download_url = None
                
                # Find the zip asset
                for asset in data.get('assets', []):
                    if asset.get('name', '').endswith('.zip'):
                        download_url = asset.get('browser_download_url')
                        break
                
                if not download_url:
                    log("Error: No zip file found in release assets")
                    self.report({'ERROR'}, "No zip file found in release assets")
                    return {'CANCELLED'}
                
                log(f"Downloading update from {download_url}")
                
                # Download the zip file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as temp_file:
                    temp_path = temp_file.name
                    
                    try:
                        with urllib.request.urlopen(download_url, timeout=30) as response:
                            # Download with progress reporting
                            total_size = int(response.info().get('Content-Length', 0))
                            downloaded = 0
                            block_size = 8192
                            
                            while True:
                                buffer = response.read(block_size)
                                if not buffer:
                                    break
                                
                                downloaded += len(buffer)
                                temp_file.write(buffer)
                                
                                # Report progress
                                if total_size > 0:
                                    progress = int((downloaded / total_size) * 100)
                                    log(f"Download progress: {progress}%")
                    
                    except Exception as e:
                        log(f"Error downloading update: {e}")
                        self.report({'ERROR'}, f"Error downloading update: {e}")
                        os.unlink(temp_path)
                        return {'CANCELLED'}
                
                log("Download complete, installing update")
                
                # Install the update
                self.install_update(temp_path)
                
                # Clean up
                try:
                    os.unlink(temp_path)
                except:
                    pass
                
                return {'FINISHED'}
                
        except Exception as e:
            log(f"Error during update process: {e}")
            self.report({'ERROR'}, f"Error during update process: {e}")
            return {'CANCELLED'}
    
    def install_update(self, zip_path):
        # Install the update from the downloaded zip file
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
                    return
                
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
                self.refresh_ui()
                
                # Show success message
                self.report({'INFO'}, "Update installed successfully. Please restart Blender.")
                
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
    
    def refresh_ui(self):
        # Reload addon and refresh UI
        log("Refreshing UI")
        
        # Get addon directory and name
        addon_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        addon_name = os.path.basename(addon_dir)
        
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
            try:
                # Re-enable the addon
                bpy.ops.preferences.addon_enable(module=addon_module)
                log("Addon re-enabled")
            except Exception as e:
                log(f"Error re-enabling addon: {e}")
        
        # Force redraw all areas
        def force_redraw():
            for window in bpy.context.window_manager.windows:
                for area in window.screen.areas:
                    area.tag_redraw()
        
        # Schedule redraw for next frame
        bpy.app.timers.register(force_redraw, first_interval=0.1)

class SHAPEKEY_OT_cancel_update(Operator):
    bl_idname = "shapekey.cancel_update"
    bl_label = "Cancel Update"
    bl_description = "Cancel the update process"
    
    def execute(self, context):
        # Cancel update
        log("Update cancelled")
        return {'FINISHED'}

def should_check_for_updates():
    last_check = None
    
    if hasattr(bpy.context.scene, "shapekey_tools_last_update_check"):
        try:
            last_check_str = bpy.context.scene.shapekey_tools_last_update_check
            if last_check_str:
                last_check = datetime.datetime.strptime(last_check_str, "%Y-%m-%d").date()
        except:
            last_check = None
    
    if last_check is None:
        return True
    
    today = datetime.datetime.now().date()
    if today > last_check:
        return True
    
    return False

def background_update_check():
    if should_check_for_updates():
        today_str = datetime.datetime.now().strftime("%Y-%m-%d")
        bpy.context.scene.shapekey_tools_last_update_check = today_str
        
        # Run the update check in a separate thread to avoid blocking the UI
        thread = threading.Thread(target=threaded_update_check)
        thread.daemon = True
        thread.start()
    
    return None

def threaded_update_check():
    try:
        # Set update check in progress
        bpy.context.scene.shapekey_tools_update_check_in_progress = True
        
        # Get current version
        addon_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        init_file = os.path.join(addon_dir, "__init__.py")
        
        with open(init_file, 'r') as f:
            content = f.read()
        
        version_match = re.search(r'"version":\s*\((\d+),\s*(\d+),\s*(\d+)\)', content)
        if not version_match:
            log("Error: Could not determine current version")
            return
        
        current_version = (int(version_match.group(1)), int(version_match.group(2)), int(version_match.group(3)))
        log(f"Current version: {current_version[0]}.{current_version[1]}.{current_version[2]}")
        
        # Get latest version from GitHub API
        api_url = GITHUB_API_URL
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'Mozilla/5.0'
        }
        req = urllib.request.Request(api_url, headers=headers)
        
        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode('utf-8'))
                tag_name = data.get('tag_name', '')
                
                # Extract version from tag name (e.g., "v1.2.3" -> (1,2,3))
                version_match = re.search(r'v?(\d+)\.(\d+)\.(\d+)', tag_name)
                if not version_match:
                    log("Error: Could not parse version from tag name")
                    return
                
                latest_version = (int(version_match.group(1)), int(version_match.group(2)), int(version_match.group(3)))
                log(f"Latest version: {latest_version[0]}.{latest_version[1]}.{latest_version[2]}")
                
                # Check if update is needed
                is_newer = False
                if latest_version[0] > current_version[0]:
                    is_newer = True
                elif latest_version[0] == current_version[0] and latest_version[1] > current_version[1]:
                    is_newer = True
                elif latest_version[0] == current_version[0] and latest_version[1] == current_version[1] and latest_version[2] > current_version[2]:
                    is_newer = True
                
                # We need to use Blender's main thread for updating UI properties
                def update_ui_properties():
                    global _latest_tag_name
                    if is_newer:
                        _latest_tag_name = tag_name
                        version_str = f"{latest_version[0]}.{latest_version[1]}.{latest_version[2]}"
                        log(f"New version {version_str} available")
                        bpy.types.Scene.shapekey_tools_update_available = True
                        bpy.types.Scene.shapekey_tools_new_version = version_str
                    else:
                        bpy.types.Scene.shapekey_tools_update_available = False
                        log("No updates available")
                    
                    # Update is no longer in progress
                    bpy.context.scene.shapekey_tools_update_check_in_progress = False
                    
                    for window in bpy.context.window_manager.windows:
                        for area in window.screen.areas:
                            area.tag_redraw()
                    
                    def delayed_redraw():
                        for window in bpy.context.window_manager.windows:
                            for area in window.screen.areas:
                                area.tag_redraw()
                        return None
                    
                    bpy.app.timers.register(delayed_redraw, first_interval=0.5)
                    bpy.app.timers.register(delayed_redraw, first_interval=1.0)
                    
                    return None
                
                # Schedule the UI update on the main thread
                bpy.app.timers.register(update_ui_properties, first_interval=0.1)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
            log(f"Network connection error: {str(e)}")
            bpy.context.scene.shapekey_tools_update_check_in_progress = False
        except Exception as e:
            log(f"Error checking for updates: {str(e)}")
            bpy.context.scene.shapekey_tools_update_check_in_progress = False
    except Exception as e:
        log(f"Error checking for updates: {str(e)}")
        if hasattr(bpy.context.scene, "shapekey_tools_update_check_in_progress"):
            bpy.context.scene.shapekey_tools_update_check_in_progress = False
    
    return None

def enable_addon(addon_module):
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
    bpy.utils.register_class(SHAPEKEY_OT_update_from_online)
    bpy.utils.register_class(SHAPEKEY_OT_show_update_dialog)
    bpy.utils.register_class(SHAPEKEY_OT_confirm_update)
    bpy.utils.register_class(SHAPEKEY_OT_cancel_update)
    bpy.types.Scene.shapekey_tools_update_available = False
    bpy.types.Scene.shapekey_tools_new_version = ""
    
    bpy.types.Scene.shapekey_tools_last_update_check = StringProperty(
        name="Last Update Check",
        description="Date of the last update check (YYYY-MM-DD)",
        default=""
    )
    
    bpy.types.Scene.shapekey_tools_update_check_in_progress = BoolProperty(
        name="Update Check In Progress",
        description="Whether an update check is currently in progress",
        default=False
    )
    
    bpy.app.timers.register(background_update_check, first_interval=1.0)

def unregister():
    if hasattr(bpy.app.timers, "is_registered") and bpy.app.timers.is_registered(background_update_check):
        bpy.app.timers.unregister(background_update_check)
    if hasattr(bpy.types.Scene, "shapekey_tools_update_available"):
        del bpy.types.Scene.shapekey_tools_update_available
    if hasattr(bpy.types.Scene, "shapekey_tools_new_version"):
        del bpy.types.Scene.shapekey_tools_new_version
    if hasattr(bpy.types.Scene, "shapekey_tools_last_update_check"):
        del bpy.types.Scene.shapekey_tools_last_update_check
    if hasattr(bpy.types.Scene, "shapekey_tools_update_check_in_progress"):
        del bpy.types.Scene.shapekey_tools_update_check_in_progress
    
    bpy.utils.unregister_class(SHAPEKEY_OT_cancel_update)
    bpy.utils.unregister_class(SHAPEKEY_OT_confirm_update)
    bpy.utils.unregister_class(SHAPEKEY_OT_show_update_dialog)
    bpy.utils.unregister_class(SHAPEKEY_OT_update_from_online) 