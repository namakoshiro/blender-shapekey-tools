"""
blender-shapekey-tools
A Blender addon that allows adding shapekeys below the currently selected one.

Author: namakoshiro
Created: 2025/1/11
Version: 1.0.0

This addon provides three main functions:
1. Add a new empty shapekey below the currently selected one
2. Add a new shapekey from current mix state below the selected one
3. Split the selected shapekey into left (.L) and right (.R) versions

The L/R split function is particularly useful for facial expressions, where you want to:
- Convert a full-face shapekey into separate left and right versions
- Automatically handle the split based on the model's X axis
- Maintain proper vertex positions around the center line
"""

"""
PLANNED TO UPDATE:
"""

bl_info = {
    "name": "blender-shapekey-tools",
    "author": "namakoshiro",
    "version": (1, 0, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > Shapekey",
    "description": "Adds a new shapekey below the currently selected one",
    "category": "Mesh",
}

import bpy
from bpy.types import Operator, Panel
import bmesh
from mathutils import Vector
import time

class ADD_OT_shapekey_below(Operator):
    """Add an empty shapekey below the currently selected one"""
    bl_idname = "object.add_shapekey_below"
    bl_label = "New Shapekey"
    bl_description = "Add a new empty shapekey below the currently selected one"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        """Check if the operator can be executed"""
        obj = context.active_object
        return obj and obj.type == 'MESH' and obj.data.shape_keys
    
    def execute(self, context):
        obj = context.active_object
        shapekeys = obj.data.shape_keys.key_blocks
        active_index = obj.active_shape_key_index
        
        # Add a new shapekey with default name
        new_key = obj.shape_key_add(name="New Key")
        
        # Return if no valid shapekey is selected
        if active_index < 0 or active_index >= len(shapekeys) - 1:
            return {'FINISHED'}
            
        # Move the new shapekey up until it's right below the selected one
        for i in range(len(shapekeys) - 1, active_index + 1, -1):
            bpy.context.object.active_shape_key_index = i
            bpy.ops.object.shape_key_move(type='UP')
            
        # Select the newly added shapekey
        obj.active_shape_key_index = active_index + 1
        
        return {'FINISHED'}

class ADD_OT_shapekey_from_mix_below(Operator):
    """Add a shapekey from current mix state below the selected one"""
    bl_idname = "object.add_shapekey_from_mix_below"
    bl_label = "New Shapekey from Mix"
    bl_description = "Add a new shapekey from current mix state below the selected one"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        """Check if the operator can be executed"""
        obj = context.active_object
        return obj and obj.type == 'MESH' and obj.data.shape_keys
    
    def execute(self, context):
        obj = context.active_object
        active_index = obj.active_shape_key_index
        
        # Add a new shapekey from current mix state
        bpy.ops.object.shape_key_add(from_mix=True)
        
        shapekeys = obj.data.shape_keys.key_blocks
        
        # Return if no valid shapekey is selected
        if active_index < 0 or active_index >= len(shapekeys) - 1:
            return {'FINISHED'}
            
        # Move the new shapekey up until it's right below the selected one
        for i in range(len(shapekeys) - 1, active_index + 1, -1):
            bpy.context.object.active_shape_key_index = i
            bpy.ops.object.shape_key_move(type='UP')
            
        # Select the newly added shapekey
        obj.active_shape_key_index = active_index + 1
        
        return {'FINISHED'}

class ADD_OT_shapekey_split_lr(Operator):
    """Split the selected shapekey into separate left and right side shapekeys.
    The split is based on the model's X axis:
    - Positive X becomes the left side (.L)
    - Negative X becomes the right side (.R)
    - Vertices near X=0 are preserved in both shapekeys
    """
    bl_idname = "object.add_shapekey_split_lr"
    bl_label = "Split Shapekey L/R"
    bl_description = "Create left and right versions of the selected shapekey"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        """Check if the operator can be executed:
        - Must have an active mesh object
        - Object must have shapekeys
        - A shapekey other than the basis must be selected
        """
        obj = context.active_object
        return (obj and obj.type == 'MESH' and obj.data.shape_keys 
                and obj.active_shape_key_index > 0)
    
    def create_side_shapekey(self, context, source_key, side):
        """Create a new shapekey for the specified side (L or R)
        
        Args:
            context: Blender context
            source_key: The shapekey to split
            side: Either 'L' or 'R' to indicate which side to preserve
        
        The function:
        1. Creates a new shapekey named "{source_key.name}.{side}"
        2. Copies all vertex positions from the source shapekey
        3. Resets vertices on the opposite side to their basis positions:
           - For .R shapekey: resets vertices with positive X (left side)
           - For .L shapekey: resets vertices with negative X (right side)
        4. Preserves vertices near the center line (X = 0 ± threshold)
        5. Moves the new shapekey to the correct position in the list
        """
        obj = context.active_object
        active_index = obj.active_shape_key_index
        
        # Create new shapekey
        new_key = obj.shape_key_add(name=f"{source_key.name}.{side}")
        new_key.value = 0
        
        # Copy vertex positions from source
        for i, v in enumerate(new_key.data):
            v.co = source_key.data[i].co.copy()
        
        # Reset vertices on the opposite side to basis
        basis = obj.data.shape_keys.reference_key
        threshold = 0.0001  # Small threshold for middle vertices
        
        for i, v in enumerate(new_key.data):
            vert_x = obj.data.vertices[i].co.x
            
            # For .R shapekey, reset left side (positive X)
            # For .L shapekey, reset right side (negative X)
            if (side == 'R' and vert_x > threshold) or (side == 'L' and vert_x < -threshold):
                v.co = basis.data[i].co.copy()
                
        # Move the new shapekey to position
        for i in range(len(obj.data.shape_keys.key_blocks) - 1, active_index + 1, -1):
            bpy.context.object.active_shape_key_index = i
            bpy.ops.object.shape_key_move(type='UP')
    
    def execute(self, context):
        """Execute the operator:
        1. Checks for valid active shapekey
        2. Creates left side shapekey first
        3. Creates right side shapekey second
        4. Selects the left side shapekey when done
        """
        obj = context.active_object
        active_key = obj.active_shape_key
        if not active_key:
            self.report({'ERROR'}, "No active shapekey selected")
            return {'CANCELLED'}
            
        # Store original index
        original_index = obj.active_shape_key_index
        
        # Create left side first (will end up above right side)
        self.create_side_shapekey(context, active_key, 'L')
        
        # Then create right side
        self.create_side_shapekey(context, active_key, 'R')
        
        # Select the left side shapekey
        obj.active_shape_key_index = original_index + 1
        
        return {'FINISHED'}

class ADD_OT_shapekey_mirror(Operator):
    """Mirror the selected shapekey along X axis and create a new shapekey below.
    Uses Blender's built-in shapekey mirror function.
    Naming convention:
    - .R -> .L
    - .L -> .R
    - Right -> Left
    - Left -> Right
    - Otherwise adds .Mirror suffix
    """
    bl_idname = "object.add_shapekey_mirror"
    bl_label = "Mirror Shapekey"
    bl_description = "Create a mirrored version of the selected shapekey using Blender's mirror function"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        """Check if the operator can be executed"""
        obj = context.active_object
        return (obj and obj.type == 'MESH' and obj.data.shape_keys 
                and obj.active_shape_key_index > 0)
    
    def get_mirror_name(self, original_name):
        """Generate appropriate name for the mirrored shapekey
        
        Args:
            original_name: Name of the source shapekey
            
        Returns:
            String: New name following the mirroring convention
        """
        # Check for .L/.R suffix
        if original_name.endswith('.L'):
            return original_name[:-2] + '.R'
        elif original_name.endswith('.R'):
            return original_name[:-2] + '.L'
        
        # Check for Left/Right suffix
        if original_name.endswith('Left'):
            return original_name[:-4] + 'Right'
        elif original_name.endswith('Right'):
            return original_name[:-5] + 'Left'
        
        # If no recognized suffix, add .Mirror
        return original_name + '.Mirror'
    
    def execute(self, context):
        """Execute the operator:
        1. Store current shapekey info
        2. Create new shapekey from mix
        3. Apply Blender's mirror function
        4. Rename according to convention
        """
        obj = context.active_object
        active_key = obj.active_shape_key
        if not active_key:
            self.report({'ERROR'}, "No active shapekey selected")
            return {'CANCELLED'}
            
        # Store original name and index
        original_name = active_key.name
        original_index = obj.active_shape_key_index
        
        # Create new shapekey from mix (using existing operator)
        bpy.ops.object.add_shapekey_from_mix_below()
        
        # Get the newly created shapekey
        new_key = obj.active_shape_key
        
        # Apply Blender's mirror function
        bpy.ops.object.shape_key_mirror()
        
        # Rename according to convention
        new_key.name = self.get_mirror_name(original_name)
        
        return {'FINISHED'}

class VIEW3D_PT_shapekey_below(Panel):
    """Panel in the 3D Viewport's sidebar that contains our operators"""
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Shapekey"
    bl_label = "Add Below Selected"
    bl_context = "objectmode"
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def poll(cls, context):
        """Check if the panel should be visible"""
        obj = context.active_object
        return obj and obj.type == 'MESH' and obj.data.shape_keys
    
    def draw(self, context):
        """Draw the panel layout:
        1. New Shapekey button - Add an empty shapekey
        2. New Shapekey from Mix button - Add a shapekey from current mix state
        3. Split Shapekey L/R button - Split into left/right versions
        4. Mirror Shapekey button - Create mirrored version
        """
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        
        col = layout.column(align=True)
        col.operator("object.add_shapekey_below")
        col.operator("object.add_shapekey_from_mix_below")
        
        col.separator()
        col.operator("object.add_shapekey_split_lr")
        col.operator("object.add_shapekey_mirror")

# Registration
def register():
    """Register all classes"""
    bpy.utils.register_class(ADD_OT_shapekey_below)
    bpy.utils.register_class(ADD_OT_shapekey_from_mix_below)
    bpy.utils.register_class(ADD_OT_shapekey_split_lr)
    bpy.utils.register_class(ADD_OT_shapekey_mirror)
    bpy.utils.register_class(VIEW3D_PT_shapekey_below)

def unregister():
    """Unregister all classes"""
    bpy.utils.unregister_class(ADD_OT_shapekey_below)
    bpy.utils.unregister_class(ADD_OT_shapekey_from_mix_below)
    bpy.utils.unregister_class(ADD_OT_shapekey_split_lr)
    bpy.utils.unregister_class(ADD_OT_shapekey_mirror)
    bpy.utils.unregister_class(VIEW3D_PT_shapekey_below)

if __name__ == "__main__":
    register() 