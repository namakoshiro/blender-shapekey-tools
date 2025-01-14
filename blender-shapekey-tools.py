"""
blender-shapekey-tools
A small tool for one click to split or merge L/R shapekeys, and generate new shapekey below the selected item

Author: namakoshiro
Created: 2025/1/11
Version: 1.1.1
Last Updated: 2025/1/14
Blender Version: 2.80 → 4.32

Functions:
Add Empty Shapekey Below: Add a new empty shapekey below the selected one.
Add Shapekey from Mix Below: Capture the current mix as a new shapekey below the selected one.
Split Shapekey L/R: Split a shapekey into left (.L) and right (.R) versions below the selected one.
Mirror Shapekey: Generate a mirrored version of the selected shapekey below the selected one.
Smart Split Mouth L/R: Experimental: Smartly split mouth shapekey into L/R.
"""

bl_info = {
    "name": "blender-shapekey-tools",
    "author": "namakoshiro",
    "version": (1, 1, 1),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Shapekey",
    "description": "A small tool for one click to split or merge L/R shapekeys, and generate new shapekey below the selected item",
    "category": "Object",
}

import bpy
from bpy.types import Operator, Panel
import bmesh
from mathutils import Vector
import time

class ADD_OT_shapekey_below(Operator):
    """Generate new empty shapekey below the selected item
    
    This operator creates a new empty shapekey and positions it 
    directly below the currently selected shapekey. It preserves
    the values of existing shapekeys during the operation.
    """
    bl_idname = "object.add_shapekey_below"
    bl_label = "New Empty Shapekey"
    bl_description = "Generate new empty shapekey below the selected item"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj and obj.type == 'MESH' and obj.data.shape_keys
    
    def execute(self, context):
        try:
            context.window_manager.progress_begin(0, 100)
            
            obj = context.active_object
            shapekeys = obj.data.shape_keys.key_blocks
            active_index = obj.active_shape_key_index
            
            # Store original values
            original_values = {sk.name: sk.value for sk in shapekeys}
            
            # Reset all shapekey values to 0
            for sk in shapekeys:
                sk.value = 0
                
            # Add a new shapekey with default name
            new_key = obj.shape_key_add(name="New Key")
            
            context.window_manager.progress_update(50)
            
            # Return if no valid shapekey is selected
            if active_index < 0 or active_index >= len(shapekeys) - 1:
                # Restore original values before returning
                for sk in shapekeys:
                    if sk.name in original_values:
                        sk.value = original_values[sk.name]
                context.window_manager.progress_end()
                return {'FINISHED'}
                
            # Move the new shapekey up until it's right below the selected one
            for i in range(len(shapekeys) - 1, active_index + 1, -1):
                bpy.context.object.active_shape_key_index = i
                bpy.ops.object.shape_key_move(type='UP')
                
            # Select the newly added shapekey
            obj.active_shape_key_index = active_index + 1
            
            # Restore original values
            for sk in shapekeys:
                if sk.name in original_values and sk != new_key:
                    sk.value = original_values[sk.name]
            
            context.window_manager.progress_end()
            return {'FINISHED'}
            
        except Exception as e:
            if context.window_manager.progress_is_running:
                context.window_manager.progress_end()
            self.report({'ERROR'}, f"Failed to add shapekey: {str(e)}")
            return {'CANCELLED'}

class ADD_OT_shapekey_from_mix_below(Operator):
    """Generate new shapekey from current mix state
    
    This operator captures the current mixed state of all shapekeys
    and creates a new shapekey below the selected one. It then resets
    all other shapekeys to 0 and sets the new one to 1.0.
    """
    bl_idname = "object.add_shapekey_from_mix_below"
    bl_label = "New Shapekey from Mix"
    bl_description = "Generate new shapekey from mix below the selected one"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj and obj.type == 'MESH' and obj.data.shape_keys
    
    def execute(self, context):
        try:
            context.window_manager.progress_begin(0, 100)
            
            obj = context.active_object
            active_index = obj.active_shape_key_index
            
            # Add a new shapekey from current mix state
            bpy.ops.object.shape_key_add(from_mix=True)
            
            context.window_manager.progress_update(30)
            
            shapekeys = obj.data.shape_keys.key_blocks
            
            # Return if no valid shapekey is selected
            if active_index < 0 or active_index >= len(shapekeys) - 1:
                context.window_manager.progress_end()
                return {'FINISHED'}
                
            # Move the new shapekey up until it's right below the selected one
            for i in range(len(shapekeys) - 1, active_index + 1, -1):
                bpy.context.object.active_shape_key_index = i
                bpy.ops.object.shape_key_move(type='UP')
                
            context.window_manager.progress_update(60)
            
            # Select the newly added shapekey
            obj.active_shape_key_index = active_index + 1
            
            # Get the new shapekey
            new_key = obj.active_shape_key
            
            # Reset all shapekey values to 0 except basis
            for sk in shapekeys:
                if sk != obj.data.shape_keys.reference_key:  # Skip basis
                    sk.value = 0
                    
            # Set the new shapekey value to 1
            new_key.value = 1.0
            
            context.window_manager.progress_end()
            return {'FINISHED'}
            
        except Exception as e:
            if context.window_manager.progress_is_running:
                context.window_manager.progress_end()
            self.report({'ERROR'}, f"Failed to add shapekey from mix: {str(e)}")
            return {'CANCELLED'}

class ADD_OT_shapekey_split_lr(Operator):
    """Split shapekey into left and right versions
    
    This operator creates two new shapekeys (.L and .R) from the selected shapekey,
    each containing only the vertex data for their respective side. The original
    shapekey's value is set to 0 after the operation.
    """
    bl_idname = "object.add_shapekey_split_lr"
    bl_label = "Split Shapekey L/R"
    bl_description = "Split shapekey into L/R below the selected one"
    bl_options = {'REGISTER', 'UNDO'}
    
    # Add configurable properties
    threshold: bpy.props.FloatProperty(
        name="Middle Threshold",
        description="Threshold for determining middle vertices",
        default=0.0001,
        min=0.0,
        max=1.0,
        precision=4
    )
    
    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj and obj.type == 'MESH' and obj.data.shape_keys 
                and obj.active_shape_key_index > 0)
    
    def create_side_shapekey(self, context, source_key, side):
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
        
        for i, v in enumerate(new_key.data):
            vert_x = obj.data.vertices[i].co.x
            
            # For .R shapekey, reset left side (positive X)
            # For .L shapekey, reset right side (negative X)
            if (side == 'R' and vert_x > self.threshold) or (side == 'L' and vert_x < -self.threshold):
                v.co = basis.data[i].co.copy()
                
        # Move the new shapekey to position
        for i in range(len(obj.data.shape_keys.key_blocks) - 1, active_index + 1, -1):
            bpy.context.object.active_shape_key_index = i
            bpy.ops.object.shape_key_move(type='UP')
    
    def execute(self, context):
        try:
            context.window_manager.progress_begin(0, 100)
            
            obj = context.active_object
            active_key = obj.active_shape_key
            if not active_key:
                self.report({'ERROR'}, "No active shapekey selected")
                return {'CANCELLED'}
                
            # Store original index
            original_index = obj.active_shape_key_index
            
            # Create left side first (will end up above right side)
            self.create_side_shapekey(context, active_key, 'L')
            context.window_manager.progress_update(40)
            
            # Then create right side
            self.create_side_shapekey(context, active_key, 'R')
            context.window_manager.progress_update(80)
            
            # Set the original shapekey value to 0
            active_key.value = 0.0
            
            # Select the left side shapekey
            obj.active_shape_key_index = original_index + 1
            
            context.window_manager.progress_end()
            return {'FINISHED'}
            
        except Exception as e:
            if context.window_manager.progress_is_running:
                context.window_manager.progress_end()
            self.report({'ERROR'}, f"Failed to split shapekey: {str(e)}")
            return {'CANCELLED'}

class ADD_OT_shapekey_mirror(Operator):
    """Mirror shapekey to create its opposite side version
    
    This operator creates a mirrored version of the selected shapekey,
    automatically detecting and handling different naming conventions
    (e.g. .L/.R, Left/Right). The new shapekey is positioned below
    the selected one.
    """
    bl_idname = "object.add_shapekey_mirror"
    bl_label = "Mirror Shapekey"
    bl_description = "Mirror shapekey to a new shapekey below the selected one"
    bl_options = {'REGISTER', 'UNDO'}
    
    # Add configurable properties
    auto_rename: bpy.props.BoolProperty(
        name="Auto Rename",
        description="Automatically rename the new shapekey based on common conventions (.L/.R, Left/Right)",
        default=True
    )
    
    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj and obj.type == 'MESH' and obj.data.shape_keys 
                and obj.active_shape_key_index > 0)
    
    def get_mirror_name(self, original_name):
        if not self.auto_rename:
            return original_name + '.Mirror'
            
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
        try:
            context.window_manager.progress_begin(0, 100)
            
            obj = context.active_object
            active_key = obj.active_shape_key
            if not active_key:
                self.report({'ERROR'}, "No active shapekey selected")
                return {'CANCELLED'}
                
            shapekeys = obj.data.shape_keys.key_blocks
            active_index = obj.active_shape_key_index
            
            # Store original values
            original_values = {sk.name: sk.value for sk in shapekeys}
            
            context.window_manager.progress_update(20)
            
            # Reset all shapekey values to 0 except the one we want to mirror
            for sk in shapekeys:
                if sk != active_key:
                    sk.value = 0
            
            # Set the active shapekey value to 1 for clean mirroring
            active_key.value = 1.0
            
            context.window_manager.progress_update(40)
            
            # Create new shapekey from current state
            bpy.ops.object.shape_key_add(from_mix=True)
            
            # Move the new shapekey up until it's right below the selected one
            for i in range(len(shapekeys) - 1, active_index + 1, -1):
                bpy.context.object.active_shape_key_index = i
                bpy.ops.object.shape_key_move(type='UP')
            
            context.window_manager.progress_update(60)
            
            # Apply mirror to the new shapekey
            bpy.ops.object.shape_key_mirror()
            
            context.window_manager.progress_update(80)
            
            # Get the newly created shapekey
            new_key = obj.active_shape_key
            
            # Rename according to convention
            new_key.name = self.get_mirror_name(active_key.name)
            
            # Reset original shapekey value to 0 and set new shapekey value to 1
            active_key.value = 0
            new_key.value = 1.0
            
            # Restore other shapekeys' values
            for sk in shapekeys:
                if sk != active_key and sk != new_key:
                    sk.value = original_values.get(sk.name, 0)
            
            context.window_manager.progress_end()
            return {'FINISHED'}
            
        except Exception as e:
            if context.window_manager.progress_is_running:
                context.window_manager.progress_end()
            self.report({'ERROR'}, f"Failed to mirror shapekey: {str(e)}")
            return {'CANCELLED'}

class ADD_OT_shapekey_smart_split_mouth_lr(Operator):
    """Smart split shapekey into weighted left and right versions
    
    This operator creates two new shapekeys (.L and .R) from the selected shapekey,
    with custom weight distribution based on vertex X positions. The deformation
    on Y and Z axes is weighted using a custom curve, while X axis deformation
    remains unchanged. Only affects the main face mesh, excluding teeth and tongue.
    """
    bl_idname = "object.add_shapekey_smart_split_mouth_lr"
    bl_label = "Smart Split Mouth L/R"
    bl_description = "Experimental: Smartly split mouth shapekey into L/R"
    bl_options = {'REGISTER', 'UNDO'}
    
    # Add configurable properties
    threshold: bpy.props.FloatProperty(
        name="Middle Threshold",
        description="Threshold for determining middle vertices",
        default=0.0001,
        min=0.0,
        max=1.0,
        precision=4
    )
    
    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj and obj.type == 'MESH' and obj.data.shape_keys 
                and obj.active_shape_key_index > 0)
    
    def find_mesh_islands(self, obj):
        """Find all separate mesh islands and return their vertex indices
        
        Returns:
            List of lists, each containing vertex indices for one island
        """
        # Create BMesh
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        bm.verts.ensure_lookup_table()
        
        islands = []
        unvisited = set(range(len(bm.verts)))
        
        while unvisited:
            # Start new island
            start = unvisited.pop()
            island = {start}
            to_visit = {start}
            
            # Expand island
            while to_visit:
                current = to_visit.pop()
                vert = bm.verts[current]
                
                # Add connected vertices
                for edge in vert.link_edges:
                    other = edge.other_vert(vert)
                    other_index = other.index
                    if other_index in unvisited:
                        unvisited.remove(other_index)
                        island.add(other_index)
                        to_visit.add(other_index)
            
            islands.append(list(island))
        
        bm.free()
        return islands
    
    def get_island_bounds(self, obj, island_verts):
        """Get the bounding box of an island"""
        coords = [obj.data.vertices[i].co for i in island_verts]
        min_x = min(co.x for co in coords)
        max_x = max(co.x for co in coords)
        min_y = min(co.y for co in coords)
        max_y = max(co.y for co in coords)
        min_z = min(co.z for co in coords)
        max_z = max(co.z for co in coords)
        
        volume = (max_x - min_x) * (max_y - min_y) * (max_z - min_z)
        return {
            'volume': volume,
            'vert_count': len(island_verts),
            'verts': island_verts,
            'bounds': (min_x, max_x, min_y, max_y, min_z, max_z)
        }
    
    def find_face_mesh(self, obj):
        """Find the main face mesh by identifying the largest connected mesh"""
        islands = self.find_mesh_islands(obj)
        
        # Get bounds and metrics for each island
        island_data = [self.get_island_bounds(obj, island) for island in islands]
        
        # Sort by volume and vertex count
        island_data.sort(key=lambda x: (x['volume'], x['vert_count']), reverse=True)
        
        # Return vertices of the largest island (face mesh)
        return set(island_data[0]['verts'])
    
    def calculate_custom_weight(self, position):
        """Calculate weight using custom curve
        
        Args:
            position: Value from 0 to 1 representing position from left to right
        
        Returns:
            Weight value from 0 to 1 using a smooth bezier curve:
            - Almost flat in the first 30% (very slow decay)
            - Extremely rapid decay after 30%, approaching 0 quickly
        """
        # Bezier curve control points
        p0 = 0.0  # Start point
        p1 = 0.99  # First control point (moved to 0.99 for even flatter first 30%)
        p2 = 0.65  # Second control point (moved to 0.65 for extremely steep decay)
        p3 = 1.0  # End point
        
        # Cubic Bezier curve calculation
        t = position
        t2 = t * t
        t3 = t2 * t
        mt = 1 - t
        mt2 = mt * mt
        mt3 = mt2 * mt
        
        # Calculate weight using cubic Bezier curve
        # Moving p1 extremely close to 1.0 makes the first 30% almost completely flat
        # Moving p2 far from 1.0 creates an extremely steep drop-off
        weight = mt3 * 1.0 + 3 * mt2 * t * p1 + 3 * mt * t2 * p2 + t3 * 0.0
        
        return weight
    
    def find_deformed_vertices(self, basis_key, shape_key, face_verts):
        """Find vertices that are modified by the shapekey and are part of the face mesh"""
        deformed_verts = []
        for i, (basis_vert, shape_vert) in enumerate(zip(basis_key.data, shape_key.data)):
            if i in face_verts and (basis_vert.co - shape_vert.co).length > self.threshold:
                deformed_verts.append(i)
        return deformed_verts
    
    def get_x_range(self, vertices, deformed_indices, source_key):
        """Get the X coordinate range of deformed vertices in their deformed state"""
        x_coords = [source_key.data[i].co.x for i in deformed_indices]
        return min(x_coords), max(x_coords)
    
    def create_weighted_side_shapekey(self, context, source_key, side, deformed_indices, x_min, x_max, face_verts):
        """Create a new weighted side shapekey"""
        obj = context.active_object
        basis = obj.data.shape_keys.reference_key
        
        # Create new shapekey
        new_key = obj.shape_key_add(name=f"{source_key.name}.{side}")
        new_key.value = 0
        
        # Calculate weights and apply deformation
        x_range = x_max - x_min
        for i, v in enumerate(new_key.data):
            if i in deformed_indices:
                # Get relative position in X range using deformed position
                rel_pos = (source_key.data[i].co.x - x_min) / x_range
                
                # For right side, invert the position
                if side == 'R':
                    rel_pos = 1 - rel_pos
                
                # Calculate weight using custom curve
                weight = self.calculate_custom_weight(rel_pos)
                
                # Get the deformation vector
                deform = source_key.data[i].co - basis.data[i].co
                
                # Apply weighted deformation
                weighted_deform = Vector((
                    deform.x,  # X unchanged
                    deform.y * weight,  # Y weighted
                    deform.z * weight   # Z weighted
                ))
                
                # Apply the weighted deformation
                v.co = basis.data[i].co + weighted_deform
            else:
                # Copy the original shape for non-face vertices
                v.co = source_key.data[i].co.copy() if i not in face_verts else basis.data[i].co
    
    def execute(self, context):
        try:
            context.window_manager.progress_begin(0, 100)
            
            obj = context.active_object
            active_key = obj.active_shape_key
            if not active_key:
                self.report({'ERROR'}, "No active shapekey selected")
                return {'CANCELLED'}
            
            # Find face mesh vertices
            face_verts = self.find_face_mesh(obj)
            
            # Store original index and values
            active_index = obj.active_shape_key_index
            original_values = {sk.name: sk.value for sk in obj.data.shape_keys.key_blocks}
            
            # Find deformed vertices (only in face mesh)
            basis = obj.data.shape_keys.reference_key
            deformed_indices = self.find_deformed_vertices(basis, active_key, face_verts)
            
            if not deformed_indices:
                self.report({'ERROR'}, "No deformed vertices found in face mesh")
                return {'CANCELLED'}
            
            context.window_manager.progress_update(30)
            
            # Get X range of deformed vertices using deformed positions
            x_min, x_max = self.get_x_range(obj.data.vertices, deformed_indices, active_key)
            
            # Create right side first (will end up below left side)
            self.create_weighted_side_shapekey(context, active_key, 'R', deformed_indices, x_min, x_max, face_verts)
            
            # Move the right side shapekey up
            shapekeys = obj.data.shape_keys.key_blocks
            for i in range(len(shapekeys) - 1, active_index + 1, -1):
                bpy.context.object.active_shape_key_index = i
                bpy.ops.object.shape_key_move(type='UP')
            
            context.window_manager.progress_update(60)
            
            # Create left side
            self.create_weighted_side_shapekey(context, active_key, 'L', deformed_indices, x_min, x_max, face_verts)
            
            # Move the left side shapekey up
            shapekeys = obj.data.shape_keys.key_blocks
            for i in range(len(shapekeys) - 1, active_index + 1, -1):
                bpy.context.object.active_shape_key_index = i
                bpy.ops.object.shape_key_move(type='UP')
            
            context.window_manager.progress_update(80)
            
            # Reset original shapekey value and restore other values
            active_key.value = 0
            for sk in shapekeys:
                if sk != active_key and sk.name in original_values:
                    sk.value = original_values[sk.name]
            
            # Select the left side shapekey
            obj.active_shape_key_index = active_index + 1
            
            context.window_manager.progress_end()
            return {'FINISHED'}
            
        except Exception as e:
            if context.window_manager.progress_is_running:
                context.window_manager.progress_end()
            self.report({'ERROR'}, f"Failed to smart split shapekey: {str(e)}")
            return {'CANCELLED'}

class VIEW3D_PT_shapekey_tools(Panel):
    """Panel for Shapekey Tools
    
    This panel provides quick access to shapekey manipulation tools
    in the 3D View's sidebar. It is visible when a mesh object with
    shapekeys is selected.
    """
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Shapekey"
    bl_label = "Shapekey Tools"
    
    @classmethod
    def poll(cls, context):
        obj = context.active_object
        if not obj or obj.type != 'MESH' or not obj.data.shape_keys:
            return False
            
        # Show panel in both object mode and edit mode
        return context.mode in {'OBJECT', 'EDIT_MESH'}
    
    def draw(self, context):
        """Draw the panel layout"""
        layout = self.layout
        
        # Add mode warning if needed
        if context.mode == 'EDIT_MESH':
            box = layout.box()
            box.label(text="Warning: Exit Edit Mode to use", icon='INFO')
            box.label(text="these tools", icon='BLANK1')
            layout.separator()
        
        # Basic Operations buttons
        box = layout.box()
        col = box.column(align=True)
        col.operator("object.add_shapekey_below", icon='ADD')
        col.operator("object.add_shapekey_from_mix_below", icon='ADD')
        
        # Separator between button groups
        layout.separator()
        
        # Advanced Operations buttons
        box = layout.box()
        col = box.column(align=True)
        col.operator("object.add_shapekey_split_lr", icon='MOD_MIRROR')
        col.operator("object.add_shapekey_mirror", icon='ARROW_LEFTRIGHT')
        
        # Separator before experimental section
        layout.separator()
        
        # Experimental Operations
        box = layout.box()
        box.label(text="Experimental", icon='ERROR')
        col = box.column(align=True)
        col.operator("object.add_shapekey_smart_split_mouth_lr", icon='MOD_MIRROR')
        
        # Add version information
        layout.separator()
        box = layout.box()
        col = box.column()
        col.scale_y = 0.8
        col.label(text="Version: 1.1.1")
        col.label(text="Last Updated: 2025/1/14")
        col.label(text="Blender: 2.80 → 4.32")

def register():
    """Register all classes"""
    bpy.utils.register_class(ADD_OT_shapekey_below)
    bpy.utils.register_class(ADD_OT_shapekey_from_mix_below)
    bpy.utils.register_class(ADD_OT_shapekey_split_lr)
    bpy.utils.register_class(ADD_OT_shapekey_mirror)
    bpy.utils.register_class(ADD_OT_shapekey_smart_split_mouth_lr)
    bpy.utils.register_class(VIEW3D_PT_shapekey_tools)

def unregister():
    """Unregister all classes"""
    bpy.utils.unregister_class(VIEW3D_PT_shapekey_tools)
    bpy.utils.unregister_class(ADD_OT_shapekey_smart_split_mouth_lr)
    bpy.utils.unregister_class(ADD_OT_shapekey_mirror)
    bpy.utils.unregister_class(ADD_OT_shapekey_split_lr)
    bpy.utils.unregister_class(ADD_OT_shapekey_from_mix_below)
    bpy.utils.unregister_class(ADD_OT_shapekey_below)

if __name__ == "__main__":
    register() 
