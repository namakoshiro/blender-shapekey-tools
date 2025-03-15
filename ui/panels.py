import bpy
from bpy.types import Panel

class VIEW3D_PT_shapekey_tools(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Shapekey"
    bl_label = "Shapekey Tools"
    
    @classmethod
    def poll(cls, context):
        # Check if object is mesh with shapekeys
        obj = context.active_object
        return obj and obj.type == 'MESH' and obj.data.shape_keys
    
    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        
        # Check conditions
        is_object_mode = context.mode == 'OBJECT'
        has_active_non_basis = obj.active_shape_key_index > 0
        
        # Show warning if not in object mode
        if not is_object_mode:
            box = layout.box()
            box.alert = True
            box.label(text="Work in Object Mode", icon='ERROR')
            layout.separator()
        
        # Basic operators section
        box = layout.box()
        col = box.column(align=True)
        col.enabled = is_object_mode
        col.operator("object.add_shapekey_below", icon='ADD')
        col.operator("object.add_shapekey_from_mix_below", icon='ADD')
        
        # Only show delete unlocked button in Blender 4.20 and above
        if bpy.app.version >= (4, 2, 0):
            col.operator("object.delete_unlocked_shapekeys", icon='REMOVE')
        
        # Mirror and split operators section
        box = layout.box()
        col = box.column(align=True)
        col.enabled = is_object_mode and has_active_non_basis
        col.operator("object.add_shapekey_mirror", icon='ARROW_LEFTRIGHT')
        col.operator("object.add_shapekey_split_lr", icon='MOD_MIRROR')
        col.operator("object.add_shapekey_smooth_split_mouth_lr", icon='MOD_MIRROR')
        
        # Version and update section
        layout.separator()
        box = layout.box()
        row = box.row(align=True)
        split = row.split(factor=0.5, align=True)
        
        # Update button
        col = split.column(align=True)
        col.scale_y = 1
        col.operator("shapekey.update_from_online", text="Update", icon='URL')
        
        # Install button
        col = split.column(align=True)
        col.scale_y = 1
        col.operator("shapekey.update_from_local", text="Install", icon='PACKAGE')

        # Version Info
        col = box.column()
        col.label(text="Version: 1.3.0")
        col.label(text="Last Updated: 2025/3/14")
        if hasattr(bpy.types.Scene, "shapekey_tools_update_available"):
            if hasattr(bpy.context.scene, "shapekey_tools_update_check_in_progress") and bpy.context.scene.shapekey_tools_update_check_in_progress:
                col.label(text="Checking update...")
            elif bpy.types.Scene.shapekey_tools_update_available:
                new_version = bpy.types.Scene.shapekey_tools_new_version if hasattr(bpy.types.Scene, "shapekey_tools_new_version") else ""
                col.label(text=f"New version {new_version} available", icon='FILE_REFRESH')
            else:
                col.label(text="Already latest version", icon='CHECKMARK')
        else:
            col.label(text="")

# Register
def register():
    bpy.utils.register_class(VIEW3D_PT_shapekey_tools)

# Unregister
def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_shapekey_tools) 