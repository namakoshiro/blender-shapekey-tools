import bpy
from bpy.types import Operator
import bmesh
from mathutils import Vector

class ADD_OT_shapekey_smooth_split_mouth_lr(Operator):
    bl_idname = "object.add_shapekey_smooth_split_mouth_lr"
    bl_label = "Smoothly Split Mouth L/R"
    bl_description = "Smoothly split mouth shapekey into L/R with weighted transition"
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
        # Check if object is mesh with shapekeys and has active non-basis shapekey
        obj = context.active_object
        return (obj and obj.type == 'MESH' and obj.data.shape_keys 
                and obj.active_shape_key_index > 0)
    
    def find_mesh_islands(self, obj):
        # Create BMesh for topology analysis
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        bm.verts.ensure_lookup_table()
        
        islands = []
        unvisited = set(range(len(bm.verts)))
        
        while unvisited:
            # Start a new island from unvisited vertex
            start = unvisited.pop()
            island = {start}
            to_visit = {start}
            
            # Find all connected vertices
            while to_visit:
                current = to_visit.pop()
                vert = bm.verts[current]
                
                # Add all connected unvisited vertices
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
        # Get vertex coordinates
        coords = [obj.data.vertices[i].co for i in island_verts]
        
        # Calculate bounds
        min_x = min(co.x for co in coords)
        max_x = max(co.x for co in coords)
        min_y = min(co.y for co in coords)
        max_y = max(co.y for co in coords)
        min_z = min(co.z for co in coords)
        max_z = max(co.z for co in coords)
        
        # Calculate volume and return metrics
        volume = (max_x - min_x) * (max_y - min_y) * (max_z - min_z)
        return {
            'volume': volume,
            'vert_count': len(island_verts),
            'verts': island_verts,
            'bounds': (min_x, max_x, min_y, max_y, min_z, max_z)
        }
    
    def find_face_mesh(self, obj):
        # Get all separate mesh islands
        islands = self.find_mesh_islands(obj)
        
        # Calculate metrics for each island
        island_data = [self.get_island_bounds(obj, island) for island in islands]
        
        # Sort by volume and vertex count to find main face mesh
        island_data.sort(key=lambda x: (x['volume'], x['vert_count']), reverse=True)
        
        # Return vertices of largest island (face mesh)
        return set(island_data[0]['verts'])
    
    def calculate_custom_weight(self, position, is_upward):
        if is_upward:
            # Keep full weight in first 30% for upper lip
            if position <= 0.3:
                return 1.0
            
            # Remap position for bezier calculation
            remapped_pos = (position - 0.3) / 0.7
            
            # Extremely steep curve for upper lip
            p1 = 0.5   # Steep transition
            p2 = 0.1   # Minimal final value
        else:
            # No flat area for lower lip
            remapped_pos = position
            
            # Steeper curve for lower lip
            p1 = 0.8   # Steeper transition
            p2 = 0.4   # Higher final value
        
        # Calculate bezier curve weight
        p0 = 0.0  # Start point
        p3 = 1.0  # End point
        t = remapped_pos
        t2 = t * t
        t3 = t2 * t
        mt = 1 - t
        mt2 = mt * mt
        mt3 = mt2 * mt
        
        # Get raw weight and remap to 0.1-1.0 range
        raw_weight = mt3 * 1.0 + 3 * mt2 * t * p1 + 3 * mt * t2 * p2 + t3 * 0.0
        return 0.1 + raw_weight * (1.0 - 0.1)
    
    def find_deformed_vertices(self, basis_key, shape_key, face_verts):
        face_deformed = []
        non_face_deformed = []
        
        # Check each vertex for deformation
        for i, (basis_vert, shape_vert) in enumerate(zip(basis_key.data, shape_key.data)):
            if (basis_vert.co - shape_vert.co).length > self.threshold:
                if i in face_verts:
                    face_deformed.append(i)
                else:
                    non_face_deformed.append(i)
        
        return face_deformed, non_face_deformed
    
    def get_x_range(self, vertices, deformed_indices, source_key):
        # Get X coordinates of deformed vertices
        x_coords = [source_key.data[i].co.x for i in deformed_indices]
        return min(x_coords), max(x_coords)
    
    def create_weighted_side_shapekey(self, context, source_key, side, deformed_indices, x_min, x_max, face_verts, non_face_deformed):
        obj = context.active_object
        basis = obj.data.shape_keys.reference_key
        
        # Create new shapekey with side suffix
        new_key = obj.shape_key_add(name=f"{source_key.name}.{side}")
        new_key.value = 0
        
        # Calculate weights and apply deformation
        x_range = x_max - x_min
        for i, v in enumerate(new_key.data):
            if i in deformed_indices:  # Face mesh vertices
                # Calculate relative position and weight
                rel_pos = (source_key.data[i].co.x - x_min) / x_range
                if side == 'L':
                    rel_pos = 1 - rel_pos
                
                # Get deformation and weight
                deform = source_key.data[i].co - basis.data[i].co
                is_upward = deform.z > 0
                z_weight = self.calculate_custom_weight(rel_pos, is_upward)
                
                # Calculate side weight
                xy_weight = 1.0
                vert_x = source_key.data[i].co.x
                if (side == 'L' and vert_x < 0) or (side == 'R' and vert_x > 0):
                    xy_weight = 0.5
                
                # Apply weighted deformation
                weighted_deform = Vector((
                    deform.x * xy_weight,  # Side-based X weight
                    deform.y * z_weight,   # Vertical transition weight
                    deform.z * z_weight    # Vertical transition weight
                ))
                v.co = basis.data[i].co + weighted_deform
                
            elif i in non_face_deformed:  # Teeth and tongue
                # Scale down non-face deformation
                v.co = basis.data[i].co + (source_key.data[i].co - basis.data[i].co) * 0.5
                
            else:  # Undeformed vertices
                # Keep original or basis shape
                v.co = source_key.data[i].co.copy() if i not in face_verts else basis.data[i].co
    
    def execute(self, context):
        try:
            context.window_manager.progress_begin(0, 100)
            
            obj = context.active_object
            active_key = obj.active_shape_key
            if not active_key:
                self.report({'ERROR'}, "No active shapekey selected")
                return {'CANCELLED'}
            
            # Find face mesh and deformed vertices
            face_verts = self.find_face_mesh(obj)
            active_index = obj.active_shape_key_index
            basis = obj.data.shape_keys.reference_key
            deformed_indices, non_face_deformed = self.find_deformed_vertices(basis, active_key, face_verts)
            
            if not deformed_indices:
                self.report({'ERROR'}, "No deformed vertices found in face mesh")
                return {'CANCELLED'}
            
            context.window_manager.progress_update(30)
            
            # Get deformation range and create right side
            x_min, x_max = self.get_x_range(obj.data.vertices, deformed_indices, active_key)
            self.create_weighted_side_shapekey(context, active_key, 'R', deformed_indices, x_min, x_max, face_verts, non_face_deformed)
            
            # Position right side shapekey
            shapekeys = obj.data.shape_keys.key_blocks
            for i in range(len(shapekeys) - 1, active_index + 1, -1):
                bpy.context.object.active_shape_key_index = i
                bpy.ops.object.shape_key_move(type='UP')
            
            context.window_manager.progress_update(60)
            
            # Create and position left side
            self.create_weighted_side_shapekey(context, active_key, 'L', deformed_indices, x_min, x_max, face_verts, non_face_deformed)
            for i in range(len(shapekeys) - 1, active_index + 1, -1):
                bpy.context.object.active_shape_key_index = i
                bpy.ops.object.shape_key_move(type='UP')
            
            context.window_manager.progress_update(80)
            
            # Set values and selection
            active_key.value = 0  # Reset original
            left_key = obj.data.shape_keys.key_blocks[active_index + 1]
            right_key = obj.data.shape_keys.key_blocks[active_index + 2]
            left_key.value = 1.0  # Show left side
            right_key.value = 0.0  # Hide right side
            obj.active_shape_key_index = active_index + 1  # Select left side
            
            context.window_manager.progress_end()
            return {'FINISHED'}
            
        except Exception as e:
            if context.window_manager.progress_is_running:
                context.window_manager.progress_end()
            self.report({'ERROR'}, f"Failed to smooth split shapekey: {str(e)}")
            return {'CANCELLED'}

# Register
def register():
    bpy.utils.register_class(ADD_OT_shapekey_smooth_split_mouth_lr)

# Unregister
def unregister():
    bpy.utils.unregister_class(ADD_OT_shapekey_smooth_split_mouth_lr) 