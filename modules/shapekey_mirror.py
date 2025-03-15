import bpy
from bpy.types import Operator

class ADD_OT_shapekey_mirror(Operator):
    bl_idname = "object.add_shapekey_mirror"
    bl_label = "Mirror Shapekey"
    bl_description = "Mirror shapekey to a new shapekey below the selected"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        # Check if object is mesh with shapekeys and has active non-basis shapekey
        obj = context.active_object
        return (obj and obj.type == 'MESH' and obj.data.shape_keys 
                and obj.active_shape_key_index > 0)
    
    def get_mirror_name(self, original_name):
        # Check single character suffix (.L/.R)
        if original_name.endswith('.L'):
            return original_name[:-2] + '.R'
        if original_name.endswith('.R'):
            return original_name[:-2] + '.L'
            
        # Check Chinese characters (左/右)
        if original_name.endswith('左'):
            return original_name[:-1] + '右'
        if original_name.endswith('右'):
            return original_name[:-1] + '左'
            
        # Check English words (case insensitive)
        lower_name = original_name.lower()
        if lower_name.endswith('left'):
            return original_name[:-4] + 'Right'
        if lower_name.endswith('right'):
            return original_name[:-5] + 'Left'
            
        # If no recognized suffix, keep original name
        return original_name
    
    def execute(self, context):
        try:
            obj = context.active_object
            active_key = obj.active_shape_key
            if not active_key:
                self.report({'ERROR'}, "No active shapekey selected")
                return {'CANCELLED'}
                
            # Store original index for positioning
            active_index = obj.active_shape_key_index
            
            # Set the active shapekey value to 1 for clean mirroring
            active_key.value = 1.0
            
            # Create new shapekey from current state
            bpy.ops.object.shape_key_add(from_mix=True)
            
            # Position it below the selected shapekey
            for i in range(len(obj.data.shape_keys.key_blocks) - 1, active_index + 1, -1):
                bpy.context.object.active_shape_key_index = i
                bpy.ops.object.shape_key_move(type='UP')
            
            # Apply mirror to the new shapekey
            bpy.ops.object.shape_key_mirror()
            
            # Get the newly created shapekey and rename it
            new_key = obj.active_shape_key
            new_key.name = self.get_mirror_name(active_key.name)
            
            # Set original shapekey value to 0 and new shapekey value to 1
            active_key.value = 0
            new_key.value = 1.0
            
            # Select the new mirrored shapekey
            obj.active_shape_key_index = active_index + 1
            
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Failed to mirror shapekey: {str(e)}")
            return {'CANCELLED'}

# Register
def register():
    bpy.utils.register_class(ADD_OT_shapekey_mirror)

# Unregister
def unregister():
    bpy.utils.unregister_class(ADD_OT_shapekey_mirror) 