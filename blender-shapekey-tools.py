##  Manual
##  *The following languages are arranged in alphabetical order
##  
##  English
##  - New Empty Shapekey: Add a new empty shapekey below the selected.
##  - New Shapekey from Mix: Capture the current mix as a new shapekey below the selected.
##  - Delete All Except Locked (for Blender ≥ 4.2): Delete all shapekeys except basis and locked ones.
##  - Mirror Shapekey: Generate a mirrored version of the selected shapekey below the selected.
##  - Split Shapekey L/R: Split a shapekey into left (.L) and right (.R) versions below the selected.
##  - Smoothly Split Mouth L/R: Smoothly split mouth shapekey into L/R with weighted transition. Teeth and tongue animations will be scaled down but won't be tilted like lips.
##  
##  Español
##  - New Empty Shapekey: Crear un nuevo shapekey vacío debajo del seleccionado.
##  - New Shapekey from Mix: Capturar la mezcla actual como nuevo shapekey debajo del seleccionado.
##  - Delete All Except Locked (for Blender ≥ 4.2): Eliminar todos los shapekeys excepto basis y los bloqueados.
##  - Mirror Shapekey: Generar una versión espejo del shapekey debajo del seleccionado.
##  - Split Shapekey L/R: Dividir el shapekey en versiones izquierda (.L) y derecha (.R) debajo del seleccionado.
##  - Smoothly Split Mouth L/R: Dividir suavemente el shapekey de boca en L/R con transición ponderada. Las animaciones de dientes y lengua se reducirán pero no se inclinarán como los labios.
##  
##  Japanese
##  - New Empty Shapekey: 新しい空のshapekeyを選択したものの下に作成します。
##  - New Shapekey from Mix: 現在の混合状態からshapekeyを選択したものの下に作成します。
##  - Delete All Except Locked (for Blender ≥ 4.2): basis及びロックされたshapekey以外のすべてのshapekeyを削除します。
##  - Mirror Shapekey: shapekeyのミラーバージョンを選択したものの下に作成します。
##  - Split Shapekey L/R: shapekeyを左(.L)右(.R)バージョンに分割して選択したものの下に作成します。
##  - Smoothly Split Mouth L/R: 口のshapekeyを重み付き遷移でL/Rに滑らかに分割します。歯と舌のアニメーションは縮小されますが、唇のように傾斜しません。
##  
##  Korean
##  - New Empty Shapekey: 새로운 빈 shapekey를 선택한 항목 아래에 생성합니다.
##  - New Shapekey from Mix: 현재 혼합 상태의 shapekey를 선택한 항목 아래에 생성합니다.
##  - Delete All Except Locked (for Blender ≥ 4.2): basis와 잠긴 shapekey를 제외한 모든shapekey를 삭제합니다.
##  - Mirror Shapekey: shapekey의 미러 버전을 선택한 항목 아래에 생성합니다.
##  - Split Shapekey L/R: shapekey를 좌(.L)우(.R) 버전으로 분할하여 선택한 항목 아래에 생성합니다.
##  - Smoothly Split Mouth L/R: 입 shapekey를 가중치 전환으로 L/R로 부드럽게 분할합니다. 치아와 혀의 애니메이션은 축소되지만 입술처럼 기울어지지 않습니다.
##  
##  Simplified Chinese
##  - New Empty Shapekey: 创建一个空白shapekey在选中项下方。
##  - New Shapekey from Mix: 将当前混合状态保存为shapekey在选中项下方。
##  - Delete All Except Locked (for Blender ≥ 4.2): 删除除basis和已锁定以外的所有shapekey。
##  - Mirror Shapekey: 创建选中shapekey的镜像版本在选中项下方。
##  - Split Shapekey L/R: 将shapekey拆分为左(.L)右(.R)两个版本在选中项下方。
##  - Smoothly Split Mouth L/R: 将嘴部shapekey平滑拆分为带权重过渡的L/R版本。牙齿和舌头的动画幅度也会缩小，但不会像嘴唇一样倾斜。
##  
##  Traditional Chinese
##  - New Empty Shapekey: 創建一個空白shapekey在所選項目下方。
##  - New Shapekey from Mix: 將當前混合狀態儲存為shapekey在所選項目下方。
##  - Delete All Except Locked (for Blender ≥ 4.2): 刪除除basis和已鎖定以外的所有shapekey。
##  - Mirror Shapekey: 創建所選shapekey的鏡像版本在所選項目下方。
##  - Split Shapekey L/R: 將shapekey分割為左(.L)右(.R)兩個版本在所選項目下方。
##  - Smoothly Split Mouth L/R: 將嘴部shapekey平滑分割為帶權重過渡的L/R版本。牙齒和舌头的动画幅度也會縮小，但不會像嘴唇一樣傾斜。
"""
A blender add-on for one-click to split or merge L/R shapekeys, and create new shapekey below the selected.

Features:
- Create empty shapekey below the selected
- Create shapekey from mix below the selected
- Delete all shapekey except locked and basis
- Mirror shapekey
- Split shapekey into L/R
- Smoothly split mouth shapekey into L/R

Version: 1.2.1
Created: 2025/1/11
Last Updated: 2025/1/16
Support Blender Version: 2.80 → 4.3

GPL License
Blender Add-on | Blender Shapekey Tools

Copyright (C) 2025 namakoshiro

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

bl_info = {
    "name": "Blender Shapekey Tools",
    "author": "namakoshiro",
    "version": (1, 2, 1),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Shapekey",
    "description": "A blender add-on for one-click to split or merge L/R shapekeys",
    "warning": "",
    "wiki_url": "https://github.com/namakoshiro/blender-shapekey-tools",
    "doc_url": "https://github.com/namakoshiro/blender-shapekey-tools",
    "category": "Object",
    "support": "COMMUNITY"
}

import bpy
from bpy.types import Operator, Panel
import bmesh
from mathutils import Vector
import time

class ADD_OT_shapekey_below(Operator):
    """Generate new empty shapekey below the selected
    
    - Create a new empty shapekey named 'New Key'
    - Position it below the selected shapekey
    - Select the new shapekey
    """
    bl_idname = "object.add_shapekey_below"
    bl_label = "New Empty Shapekey"
    bl_description = "Generate new empty shapekey below the selected"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
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

class ADD_OT_shapekey_from_mix_below(Operator):
    """Generate new shapekey from current mix state
    
    - Create a new shapekey named 'New Mix Key' from current mix state
    - Position it below the selected shapekey
    - Reset all shapekey values to 0
    - Set the new shapekey value to 1
    - Select the new mix shapekey
    """
    bl_idname = "object.add_shapekey_from_mix_below"
    bl_label = "New Shapekey from Mix"
    bl_description = "Generate new shapekey from mix below the selected"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
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

class DELETE_OT_unlocked_shapekeys(Operator):
    """Delete all shapekey except locked and basis
    
    - Delete all shapekeys except basis and locked ones
    - Keep selection on locked shapekey if it was selected
    - Select basis if unlocked shapekey was selected
    - Report number of deleted and locked shapekeys
    """
    bl_idname = "object.delete_unlocked_shapekeys"
    bl_label = "Delete All Except Locked"
    bl_description = "Delete all except locked ones and basis"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
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

class ADD_OT_shapekey_mirror(Operator):
    """Mirror shapekey to create its opposite side version
    
    - Create a new shapekey with mirrored shape
    - Auto rename by swapping L/R, 左/右, Left/Right suffix
    - Position it below the selected shapekey
    - Set original shapekey value to 0
    - Set the new shapekey value to 1
    - Select the new mirrored shapekey
    """
    bl_idname = "object.add_shapekey_mirror"
    bl_label = "Mirror Shapekey"
    bl_description = "Mirror shapekey to a new shapekey below the selected"
    bl_options = {'REGISTER', 'UNDO'}
    
    def get_mirror_name(self, original_name):
        """Get mirrored name by swapping L/R, 左/右, Left/Right suffix"""
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

class ADD_OT_shapekey_split_lr(Operator):
    """Split shapekey into left and right versions
    
    - Create two new shapekeys with .L and .R suffix
    - Copy vertices animation from the selected shapekey
    - Reset opposite sides to basis shape
    - Position both below the selected shapekey
    - Set original shapekey value to 0
    - Select the .L shapekey
    """
    bl_idname = "object.add_shapekey_split_lr"
    bl_label = "Split Shapekey L/R"
    bl_description = "Split shapekey into L/R below the selected"
    bl_options = {'REGISTER', 'UNDO'}
    
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
                
        # Position the new shapekey below the selected one
        for i in range(len(obj.data.shape_keys.key_blocks) - 1, active_index + 1, -1):
            bpy.context.object.active_shape_key_index = i
            bpy.ops.object.shape_key_move(type='UP')
    
    def execute(self, context):
        try:
            obj = context.active_object
            active_key = obj.active_shape_key
            if not active_key:
                self.report({'ERROR'}, "No active shapekey selected")
                return {'CANCELLED'}
                
            # Store original index for positioning
            original_index = obj.active_shape_key_index
            
            # Create .L shapekey first (will be positioned above .R)
            self.create_side_shapekey(context, active_key, 'L')
            
            # Create .R shapekey
            self.create_side_shapekey(context, active_key, 'R')
            
            # Set original shapekey value to 0
            active_key.value = 0.0
            
            # Get the .L and .R shapekeys
            left_key = obj.data.shape_keys.key_blocks[original_index + 1]
            right_key = obj.data.shape_keys.key_blocks[original_index + 2]
            
            # Initialize values (.L = 1.0, .R = 0.0)
            left_key.value = 1.0
            right_key.value = 0.0
            
            # Select the .L shapekey
            obj.active_shape_key_index = original_index + 1
            
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Failed to split shapekey: {str(e)}")
            return {'CANCELLED'}

class ADD_OT_shapekey_smooth_split_mouth_lr(Operator):
    """Smoothly split mouth shapekey into left and right versions
    
    - Create two new shapekeys with .L and .R suffix
    - Apply custom weight transition based on vertex X positions
    - Scale down teeth and tongue animations without tilting
    - Position both below the selected shapekey
    - Set original shapekey value to 0
    - Select the .L shapekey
    """
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
        obj = context.active_object
        return (obj and obj.type == 'MESH' and obj.data.shape_keys 
                and obj.active_shape_key_index > 0)
    
    def find_mesh_islands(self, obj):
        """Find all separate mesh islands and return their vertex indices"""
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
        """Calculate bounding box and metrics for mesh island"""
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
        """Find main face mesh by identifying largest connected mesh"""
        # Get all separate mesh islands
        islands = self.find_mesh_islands(obj)
        
        # Calculate metrics for each island
        island_data = [self.get_island_bounds(obj, island) for island in islands]
        
        # Sort by volume and vertex count to find main face mesh
        island_data.sort(key=lambda x: (x['volume'], x['vert_count']), reverse=True)
        
        # Return vertices of largest island (face mesh)
        return set(island_data[0]['verts'])
    
    def calculate_custom_weight(self, position, is_upward):
        """Calculate transition weight for vertex position"""
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
        """Find vertices modified by shapekey in face and non-face areas"""
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
        """Get X coordinate range of deformed vertices"""
        # Get X coordinates of deformed vertices
        x_coords = [source_key.data[i].co.x for i in deformed_indices]
        return min(x_coords), max(x_coords)
    
    def create_weighted_side_shapekey(self, context, source_key, side, deformed_indices, x_min, x_max, face_verts, non_face_deformed):
        """Create new weighted side shapekey with custom transition"""
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
            box.label(text="Object Mode Only", icon='ERROR')
            layout.separator()
        
        # Basic Operations buttons
        box = layout.box()
        col = box.column(align=True)
        col.operator("object.add_shapekey_below", icon='ADD')
        col.operator("object.add_shapekey_from_mix_below", icon='ADD')
        
        # Only show delete unlocked button in Blender 4.20 and above
        if bpy.app.version >= (4, 2, 0):
            col.operator("object.delete_unlocked_shapekeys", icon='REMOVE')
        
        # Separator between button groups
        layout.separator()
        
        # Advanced Operations buttons
        box = layout.box()
        col = box.column(align=True)
        col.operator("object.add_shapekey_mirror", icon='ARROW_LEFTRIGHT')
        col.operator("object.add_shapekey_split_lr", icon='MOD_MIRROR')
        col.operator("object.add_shapekey_smooth_split_mouth_lr", icon='MOD_MIRROR')
        
        # Add version information
        layout.separator()
        box = layout.box()
        col = box.column()
        col.scale_y = 0.8
        col.label(text="Version: 1.2.1")
        col.label(text="Last Updated: 2025/1/16")
        col.label(text="Blender: 2.80 → 4.3")

def register():
    """Register all classes"""
    bpy.utils.register_class(ADD_OT_shapekey_below)
    bpy.utils.register_class(ADD_OT_shapekey_from_mix_below)
    bpy.utils.register_class(DELETE_OT_unlocked_shapekeys)
    bpy.utils.register_class(ADD_OT_shapekey_mirror)
    bpy.utils.register_class(ADD_OT_shapekey_split_lr)
    bpy.utils.register_class(ADD_OT_shapekey_smooth_split_mouth_lr)
    bpy.utils.register_class(VIEW3D_PT_shapekey_tools)

def unregister():
    """Unregister all classes"""
    bpy.utils.unregister_class(VIEW3D_PT_shapekey_tools)
    bpy.utils.unregister_class(ADD_OT_shapekey_smooth_split_mouth_lr)
    bpy.utils.unregister_class(ADD_OT_shapekey_split_lr)
    bpy.utils.unregister_class(ADD_OT_shapekey_mirror)
    bpy.utils.unregister_class(DELETE_OT_unlocked_shapekeys)
    bpy.utils.unregister_class(ADD_OT_shapekey_from_mix_below)
    bpy.utils.unregister_class(ADD_OT_shapekey_below)

if __name__ == "__main__":
    register() 
