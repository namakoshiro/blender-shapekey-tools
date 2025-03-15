import bpy
from bpy.types import Operator

class ADD_OT_shapekey_from_mix_below(Operator):
    bl_idname = "object.add_shapekey_from_mix_below"
    bl_label = "New Shapekey from Mix"
    bl_description = "Generate new shapekey from mix below the selected"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        # Check if object is mesh with shapekeys
        obj = context.active_object
        return obj and obj.type == 'MESH' and obj.data.shape_keys
    
    def execute(self, context):
        try:
            obj = context.active_object
            active_index = obj.active_shape_key_index
            
            # Create a new shapekey named 'New Mix Key' from current mix state
            bpy.ops.object.shape_key_add(from_mix=True)
            obj.active_shape_key.name = "New Mix Key"
            
            # Position it below the selected shapekey
            for i in range(len(obj.data.shape_keys.key_blocks) - 1, active_index + 1, -1):
                bpy.context.object.active_shape_key_index = i
                bpy.ops.object.shape_key_move(type='UP')
            
            new_key = obj.active_shape_key
            
            # Reset all shapekey values to 0
            for sk in obj.data.shape_keys.key_blocks:
                if sk != obj.data.shape_keys.reference_key:  # Skip basis
                    sk.value = 0
                
            # Set the new shapekey value to 1
            new_key.value = 1.0
            
            # Select the new mix shapekey
            obj.active_shape_key_index = active_index + 1
            
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Failed to add shapekey from mix: {str(e)}")
            return {'CANCELLED'}

# Register
def register():
    bpy.utils.register_class(ADD_OT_shapekey_from_mix_below)

# Unregister
def unregister():
    bpy.utils.unregister_class(ADD_OT_shapekey_from_mix_below) 