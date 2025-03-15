import bpy
from bpy.types import Operator

class ADD_OT_shapekey_split_lr(Operator):
    bl_idname = "object.add_shapekey_split_lr"
    bl_label = "Split Shapekey L/R"
    bl_description = "Split shapekey into L/R below the selected"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        # Check if object is mesh with shapekeys and has active non-basis shapekey
        obj = context.active_object
        return (obj and obj.type == 'MESH' and obj.data.shape_keys 
                and obj.active_shape_key_index > 0)
    
    def create_side_shapekey(self, context, source_key, side):
        obj = context.active_object
        active_index = obj.active_shape_key_index
        
        # Create new shapekey with .L or .R suffix
        new_key = obj.shape_key_add(name=f"{source_key.name}.{side}")
        new_key.value = 0
        
        # Copy all vertex positions from source shapekey
        for i, v in enumerate(new_key.data):
            v.co = source_key.data[i].co.copy()
        
        # Get basis shape for resetting vertices
        basis = obj.data.shape_keys.reference_key
        
        # Reset vertices on opposite side to basis shape
        for i, v in enumerate(new_key.data):
            vert_x = obj.data.vertices[i].co.x
            
            # Reset left side for .R version, right side for .L version
            if (side == 'R' and vert_x > 0.0001) or (side == 'L' and vert_x < -0.0001):
                v.co = basis.data[i].co.copy()
    
    def execute(self, context):
        try:
            obj = context.active_object
            active_key = obj.active_shape_key
            if not active_key:
                self.report({'ERROR'}, "No active shapekey selected")
                return {'CANCELLED'}
                
            # Store original index for positioning
            active_index = obj.active_shape_key_index
            
            # Create .R shapekey first
            self.create_side_shapekey(context, active_key, 'R')
            
            # Position right side shapekey below the active one
            shapekeys = obj.data.shape_keys.key_blocks
            for i in range(len(shapekeys) - 1, active_index + 1, -1):
                bpy.context.object.active_shape_key_index = i
                bpy.ops.object.shape_key_move(type='UP')
            
            # Create .L shapekey second
            self.create_side_shapekey(context, active_key, 'L')
            
            # Position left side shapekey below the active one (which will put it above R)
            for i in range(len(shapekeys) - 1, active_index + 1, -1):
                bpy.context.object.active_shape_key_index = i
                bpy.ops.object.shape_key_move(type='UP')
            
            # Set original shapekey value to 0
            active_key.value = 0.0
            
            # Get the .L and .R shapekeys
            left_key = obj.data.shape_keys.key_blocks[active_index + 1]
            right_key = obj.data.shape_keys.key_blocks[active_index + 2]
            
            # Initialize values (.L = 1.0, .R = 0.0)
            left_key.value = 1.0
            right_key.value = 0.0
            
            # Select the .L shapekey
            obj.active_shape_key_index = active_index + 1
            
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Failed to split shapekey: {str(e)}")
            return {'CANCELLED'}

# Register
def register():
    bpy.utils.register_class(ADD_OT_shapekey_split_lr)

# Unregister
def unregister():
    bpy.utils.unregister_class(ADD_OT_shapekey_split_lr) 