import bpy
from bpy.types import Operator
import bmesh
from mathutils import Vector

class SELECT_OT_affected_vertices(Operator):
    bl_idname = "object.select_affected_vertices"
    bl_label = "Select All Affected Vertices"
    bl_description = "Select all affected vertices of the selected shapekey in Edit Mode"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        # Check if object is mesh with shapekeys and in edit mode
        obj = context.active_object
        return (obj and obj.type == 'MESH' and obj.data.shape_keys 
                and context.mode == 'EDIT_MESH' and obj.active_shape_key_index > 0)
    
    def execute(self, context):
        try:
            obj = context.active_object
            shape_keys = obj.data.shape_keys
            if not shape_keys:
                return {'CANCELLED'}
            
            # Get the selected shapekey
            active_key_index = obj.active_shape_key_index
            if active_key_index <= 0:  # Skip basis
                self.report({'WARNING'}, "Please select a shapekey")
                return {'CANCELLED'}
            
            active_key = shape_keys.key_blocks[active_key_index]
            basis_key = shape_keys.key_blocks[0]
            
            # Get mesh data
            bm = bmesh.from_edit_mesh(obj.data)
            
            # Deselect all vertices first
            for v in bm.verts:
                v.select = False
            
            # Threshold for considering a vertex affected (can be adjusted)
            threshold = 0.0001
            
            # Count affected vertices
            affected_count = 0
            
            # Compare active shapekey with basis and select affected vertices
            for i, (basis_co, active_co) in enumerate(zip(basis_key.data, active_key.data)):
                # Calculate difference vector
                diff = Vector(active_co.co) - Vector(basis_co.co)
                
                # If the difference is significant, select the vertex
                if diff.length > threshold:
                    bm.verts[i].select = True
                    affected_count += 1
            
            # Update the mesh
            bmesh.update_edit_mesh(obj.data)
            
            # Report results
            self.report({'INFO'}, f"Selected {affected_count} affected vertices")
            
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Failed to select vertices: {str(e)}")
            return {'CANCELLED'}

# Register
def register():
    bpy.utils.register_class(SELECT_OT_affected_vertices)

# Unregister
def unregister():
    bpy.utils.unregister_class(SELECT_OT_affected_vertices) 