import bpy
from bpy.types import Operator

class ADD_OT_shapekey_below(Operator):
    bl_idname = "object.add_shapekey_below"
    bl_label = "New Empty Shapekey"
    bl_description = "Generate new empty shapekey below the selected"
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
            
            # Create a new empty shapekey named 'New Key'
            bpy.ops.object.shape_key_add(from_mix=False)
            obj.active_shape_key.name = "New Key"
            
            # Position it below the selected shapekey
            for i in range(len(obj.data.shape_keys.key_blocks) - 1, active_index + 1, -1):
                bpy.context.object.active_shape_key_index = i
                bpy.ops.object.shape_key_move(type='UP')
                
            # Select the new shapekey
            obj.active_shape_key_index = active_index + 1
            
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Failed to add shapekey: {str(e)}")
            return {'CANCELLED'}

# Register
def register():
    bpy.utils.register_class(ADD_OT_shapekey_below)

# Unregister
def unregister():
    bpy.utils.unregister_class(ADD_OT_shapekey_below) 