import bpy
from bpy.types import Operator

class DELETE_OT_unlocked_shapekeys(Operator):
    bl_idname = "object.delete_unlocked_shapekeys"
    bl_label = "Delete All Except Locked"
    bl_description = "Delete all except locked ones and basis"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        # Check if object is mesh with shapekeys
        obj = context.active_object
        return obj and obj.type == 'MESH' and obj.data.shape_keys
    
    def execute(self, context):
        try:
            obj = context.active_object
            shape_keys = obj.data.shape_keys
            if not shape_keys:
                return {'CANCELLED'}
            
            # Store selection state before deletion
            active_key = obj.active_shape_key
            active_is_locked = active_key.lock_shape if active_key else False
            
            # Count locked shapekeys for report
            locked_count = len([key for key in shape_keys.key_blocks[1:] 
                             if key.lock_shape])
            
            # Collect unlocked shapekeys to delete
            keys_to_remove = [key for key in shape_keys.key_blocks[1:] 
                            if not key.lock_shape]
            
            deleted_count = len(keys_to_remove)
            
            # Delete all unlocked shapekeys at once
            for key in keys_to_remove:
                obj.shape_key_remove(key)
            
            # Restore selection based on previous state
            if active_is_locked:
                # Keep selection on the locked shapekey
                for i, key in enumerate(shape_keys.key_blocks):
                    if key == active_key:
                        obj.active_shape_key_index = i
                        break
            else:
                # Select basis if unlocked shapekey was selected
                obj.active_shape_key_index = 0
            
            # Report deletion results
            self.report({'INFO'}, f"Deleted {deleted_count} shapekeys except {locked_count} locked")
            
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Failed to delete shapekeys: {str(e)}")
            return {'CANCELLED'}

# Register
def register():
    bpy.utils.register_class(DELETE_OT_unlocked_shapekeys)

# Unregister
def unregister():
    bpy.utils.unregister_class(DELETE_OT_unlocked_shapekeys) 