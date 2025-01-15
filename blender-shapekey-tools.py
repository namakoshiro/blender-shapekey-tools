"""
blender-shapekey-tools

A tool for one click to split or merge L/R shapekeys, and generate new shapekey below the selected. This will save a lot of time when creating complex shapekeys.
Get latest version from: https://github.com/namakoshiro/blender-shapekey-tools

Author: namakoshiro
Created: 2025/1/11
Version: 1.2.0
Last Updated: 2025/1/15
Blender Version: 2.80 → 4.32

The following languages are arranged in alphabetical order

English
- Add Empty Shapekey Below: Add a new empty shapekey below the selected.
- Add Shapekey from Mix Below: Capture the current mix as a new shapekey below the selected.
- Delete All Except Locked: Delete all shapekeys except basis and locked ones.
- Mirror Shapekey: Generate a mirrored version of the selected shapekey below the selected.
- Split Shapekey L/R: Split a shapekey into left (.L) and right (.R) versions below the selected.
- Smoothly Split Mouth L/R: Smoothly split mouth shapekey into L/R with weighted transition. Teeth and tongue animations will be scaled down but won't be tilted like lips.

Español
- Add Empty Shapekey Below: Crear un nuevo shapekey vacío debajo del seleccionado.
- Add Shapekey from Mix Below: Capturar la mezcla actual como nuevo shapekey debajo del seleccionado.
- Delete All Except Locked: Eliminar todos los shapekeys excepto basis y los bloqueados.
- Mirror Shapekey: Generar una versión espejo del shapekey debajo del seleccionado.
- Split Shapekey L/R: Dividir el shapekey en versiones izquierda (.L) y derecha (.R) debajo del seleccionado.
- Smoothly Split Mouth L/R: Dividir suavemente el shapekey de boca en L/R con transición ponderada. Las animaciones de dientes y lengua se reducirán pero no se inclinarán como los labios.

Japanese
- Add Empty Shapekey Below: 新しい空のshapekeyを選択したものの下に作成します。
- Add Shapekey from Mix Below: 現在の混合状態からshapekeyを選択したものの下に作成します。
- Delete All Except Locked: basis及びロックされたshapekey以外のすべてのshapekeyを削除します。
- Mirror Shapekey: shapekeyのミラーバージョンを選択したものの下に作成します。
- Split Shapekey L/R: shapekeyを左(.L)右(.R)バージョンに分割して選択したものの下に作成します。
- Smoothly Split Mouth L/R: 口のshapekeyを重み付き遷移でL/Rに滑らかに分割します。歯と舌のアニメーションは縮小されますが、唇のように傾斜しません。

Korean
- Add Empty Shapekey Below: 새로운 빈 shapekey를 선택한 항목 아래에 생성합니다.
- Add Shapekey from Mix Below: 현재 혼합 상태의 shapekey를 선택한 항목 아래에 생성합니다.
- Delete All Except Locked: basis와 잠긴 shapekey를 제외한 모든 shapekey를 삭제합니다.
- Mirror Shapekey: shapekey의 미러 버전을 선택한 항목 아래에 생성합니다.
- Split Shapekey L/R: shapekey를 좌(.L)우(.R) 버전으로 분할하여 선택한 항목 아래에 생성합니다.
- Smoothly Split Mouth L/R: 입 shapekey를 가중치 전환으로 L/R로 부드럽게 분할합니다. 치아와 혀의 애니메이션은 축소되지만 입술처럼 기울어지지 않습니다.

Simplified Chinese
- Add Empty Shapekey Below: 创建一个空白shapekey在选中项下方。
- Add Shapekey from Mix Below: 将当前混合状态保存为shapekey在选中项下方。
- Delete All Except Locked: 删除除basis和已锁定以外的所有shapekey。
- Mirror Shapekey: 创建选中shapekey的镜像版本在选中项下方。
- Split Shapekey L/R: 将shapekey拆分为左(.L)右(.R)两个版本在选中项下方。
- Smoothly Split Mouth L/R: 将嘴部shapekey平滑拆分为带权重过渡的L/R版本。牙齿和舌头的动画幅度也会缩小，但不会像嘴唇一样倾斜。

Traditional Chinese
- Add Empty Shapekey Below: 創建一個空白shapekey在所選項目下方。
- Add Shapekey from Mix Below: 將當前混合狀態儲存為shapekey在所選項目下方。
- Delete All Except Locked: 刪除除basis和已鎖定以外的所有shapekey。
- Mirror Shapekey: 創建所選shapekey的鏡像版本在所選項目下方。
- Split Shapekey L/R: 將shapekey分割為左(.L)右(.R)兩個版本在所選項目下方。
- Smoothly Split Mouth L/R: 將嘴部shapekey平滑分割為帶權重過渡的L/R版本。牙齿和舌頭的動畫幅度也會縮小，但不會像嘴唇一樣傾斜。
"""

bl_info = {
    "name": "blender-shapekey-tools",
    "author": "namakoshiro",
    "version": (1, 2, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Shapekey",
    "description": "A small tool for one click to split or merge L/R shapekeys, and generate new shapekey below the selected",
    "category": "Object",
}

import bpy
from bpy.types import Operator, Panel
import bmesh
from mathutils import Vector
import time

class ADD_OT_shapekey_below(Operator):
    """Generate new empty shapekey below the selected
    
    This operator creates a new empty shapekey and positions it 
    directly below the currently selected shapekey. It preserves
    the values of existing shapekeys during the operation.
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
    and creates a new shapekey below the selected. It then resets
    all other shapekeys to 0 and sets the new one to 1.0.
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
    bl_description = "Split shapekey into L/R below the selected"
    bl_options = {'REGISTER', 'UNDO'}
    
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
            # Keep center vertices (X=0) unchanged
            if (side == 'R' and vert_x > 0.0001) or (side == 'L' and vert_x < -0.0001):
                v.co = basis.data[i].co.copy()
                
        # Move the new shapekey to position
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
                
            # Store original index
            original_index = obj.active_shape_key_index
            
            # Create left side first (will end up above right side)
            self.create_side_shapekey(context, active_key, 'L')
            
            # Then create right side
            self.create_side_shapekey(context, active_key, 'R')
            
            # Set the original shapekey value to 0
            active_key.value = 0.0
            
            # Get the left and right side shapekeys
            left_key = obj.data.shape_keys.key_blocks[original_index + 1]
            right_key = obj.data.shape_keys.key_blocks[original_index + 2]
            
            # Set values
            left_key.value = 1.0
            right_key.value = 0.0
            
            # Select the left side shapekey
            obj.active_shape_key_index = original_index + 1
            
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Failed to split shapekey: {str(e)}")
            return {'CANCELLED'}

class ADD_OT_shapekey_mirror(Operator):
    """Mirror shapekey to create its opposite side version
    
    This operator creates a mirrored version of the selected shapekey,
    automatically detecting and handling different naming conventions
    (e.g. .L/.R, Left/Right). The new shapekey is positioned below
    the selected.
    """
    bl_idname = "object.add_shapekey_mirror"
    bl_label = "Mirror Shapekey"
    bl_description = "Mirror shapekey to a new shapekey below the selected"
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
    """Smoothly split mouth shapekey into weighted left and right versions
    
    This operator creates two new shapekeys (.L and .R) from the selected shapekey,
    with custom weight distribution based on vertex X positions. The deformation
    on Y and Z axes is weighted using a custom curve, while X axis deformation
    remains unchanged. Only affects the main face mesh, while teeth and tongue
    animations will be scaled down but won't be tilted like lips.
    """
    bl_idname = "object.add_shapekey_smart_split_mouth_lr"
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
    
    def calculate_custom_weight(self, position, is_upward):
        """Calculate weight using custom curve
        
        Args:
            position: Value from 0 to 1 representing position from left to right
            is_upward: Whether the deformation is upward (Z positive)
        
        Returns:
            Weight value from 1.0 to 0.1 using a custom curve:
            - For upward: First 30% remains at 1.0, then extremely steep decay
            - For downward: Steeper bezier curve from start to end
            - Upward: Extremely steep curve for dramatic upper lip movement
            - Downward: Steep but relatively smoother curve for lower lip
        """
        if is_upward:
            # Keep weight at 1.0 for first 30% for upward movement
            if position <= 0.3:
                return 1.0
                
            # Remap position from 0.3-1.0 range to 0-1 range for bezier calculation
            remapped_pos = (position - 0.3) / 0.7
            
            # Extremely steep curve for upward deformation
            p1 = 0.5   # Greatly reduced for extremely steep transition
            p2 = 0.1   # Minimal value for extremely steep decay
        else:
            # No flat area for downward movement
            remapped_pos = position
            
            # Steeper curve for downward deformation (but not as steep as upward)
            p1 = 0.8   # Reduced for steeper transition
            p2 = 0.4   # Reduced for steeper decay
        
        # Bezier curve control points
        p0 = 0.0  # Start point
        p3 = 1.0  # End point
        
        # Cubic Bezier curve calculation
        t = remapped_pos
        t2 = t * t
        t3 = t2 * t
        mt = 1 - t
        mt2 = mt * mt
        mt3 = mt2 * mt
        
        # Calculate raw bezier weight (0 to 1)
        raw_weight = mt3 * 1.0 + 3 * mt2 * t * p1 + 3 * mt * t2 * p2 + t3 * 0.0
        
        # Remap weight from 0-1 range to 0.1-1.0 range
        return 0.1 + raw_weight * (1.0 - 0.1)
    
    def find_deformed_vertices(self, basis_key, shape_key, face_verts):
        """Find vertices that are modified by the shapekey and are part of the face mesh,
        and also find non-face deformed vertices
        
        Returns:
            tuple: (face_deformed_verts, non_face_deformed_verts)
        """
        face_deformed = []
        non_face_deformed = []
        for i, (basis_vert, shape_vert) in enumerate(zip(basis_key.data, shape_key.data)):
            if (basis_vert.co - shape_vert.co).length > self.threshold:
                if i in face_verts:
                    face_deformed.append(i)
                else:
                    non_face_deformed.append(i)
        return face_deformed, non_face_deformed
    
    def get_x_range(self, vertices, deformed_indices, source_key):
        """Get the X coordinate range of deformed vertices in their deformed state"""
        x_coords = [source_key.data[i].co.x for i in deformed_indices]
        return min(x_coords), max(x_coords)
    
    def create_weighted_side_shapekey(self, context, source_key, side, deformed_indices, x_min, x_max, face_verts, non_face_deformed):
        """Create a new weighted side shapekey"""
        obj = context.active_object
        basis = obj.data.shape_keys.reference_key
        
        # Create new shapekey
        new_key = obj.shape_key_add(name=f"{source_key.name}.{side}")
        new_key.value = 0
        
        # Calculate weights and apply deformation
        x_range = x_max - x_min
        for i, v in enumerate(new_key.data):
            if i in deformed_indices:  # Face mesh vertices
                # Get relative position in X range using deformed position
                rel_pos = (source_key.data[i].co.x - x_min) / x_range
                
                # For right side (.R), use weight directly (weight=1 at negative X)
                # For left side (.L), invert the position (weight=1 at positive X)
                if side == 'L':
                    rel_pos = 1 - rel_pos
                
                # Get the deformation vector
                deform = source_key.data[i].co - basis.data[i].co
                
                # Determine if deformation is upward based on Z value
                is_upward = deform.z > 0
                
                # Calculate weight using custom curve for Z axis only
                z_weight = self.calculate_custom_weight(rel_pos, is_upward)
                
                # Calculate X and Y weight based on vertex position
                # For left side (.L): 1.0 on left, 0.5 on right
                # For right side (.R): 1.0 on right, 0.5 on left
                xy_weight = 1.0
                vert_x = source_key.data[i].co.x
                if (side == 'L' and vert_x < 0) or (side == 'R' and vert_x > 0):
                    xy_weight = 0.5
                
                # Apply weighted deformation
                weighted_deform = Vector((
                    deform.x * xy_weight,  # X scaled based on side
                    deform.y * z_weight,   # Y uses same weight as Z for consistency
                    deform.z * z_weight    # Z uses bezier curve weight
                ))
                
                # Apply the weighted deformation
                v.co = basis.data[i].co + weighted_deform
                
            elif i in non_face_deformed:  # Non-face deformed vertices (teeth, tongue, etc.)
                # Get the deformation vector and apply 0.5 scale to all axes
                v.co = basis.data[i].co + (source_key.data[i].co - basis.data[i].co) * 0.5
                
            else:  # Undeformed vertices
                # Copy the original shape for undeformed vertices
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
            
            # Find deformed vertices (both face and non-face)
            basis = obj.data.shape_keys.reference_key
            deformed_indices, non_face_deformed = self.find_deformed_vertices(basis, active_key, face_verts)
            
            if not deformed_indices:
                self.report({'ERROR'}, "No deformed vertices found in face mesh")
                return {'CANCELLED'}
            
            context.window_manager.progress_update(30)
            
            # Get X range of deformed vertices using deformed positions
            x_min, x_max = self.get_x_range(obj.data.vertices, deformed_indices, active_key)
            
            # Create right side first (will end up below left side)
            self.create_weighted_side_shapekey(context, active_key, 'R', deformed_indices, x_min, x_max, face_verts, non_face_deformed)
            
            # Move the right side shapekey up
            shapekeys = obj.data.shape_keys.key_blocks
            for i in range(len(shapekeys) - 1, active_index + 1, -1):
                bpy.context.object.active_shape_key_index = i
                bpy.ops.object.shape_key_move(type='UP')
            
            context.window_manager.progress_update(60)
            
            # Create left side
            self.create_weighted_side_shapekey(context, active_key, 'L', deformed_indices, x_min, x_max, face_verts, non_face_deformed)
            
            # Move the left side shapekey up
            shapekeys = obj.data.shape_keys.key_blocks
            for i in range(len(shapekeys) - 1, active_index + 1, -1):
                bpy.context.object.active_shape_key_index = i
                bpy.ops.object.shape_key_move(type='UP')
            
            context.window_manager.progress_update(80)
            
            # Set values and select left side shapekey
            active_key.value = 0  # Set original shapekey value to 0
            left_key = obj.data.shape_keys.key_blocks[active_index + 1]  # Get left side shapekey
            right_key = obj.data.shape_keys.key_blocks[active_index + 2]  # Get right side shapekey
            left_key.value = 1.0  # Set left side value to 1
            right_key.value = 0.0  # Set right side value to 0
            obj.active_shape_key_index = active_index + 1  # Select left side shapekey
            
            context.window_manager.progress_end()
            return {'FINISHED'}
            
        except Exception as e:
            if context.window_manager.progress_is_running:
                context.window_manager.progress_end()
            self.report({'ERROR'}, f"Failed to smart split shapekey: {str(e)}")
            return {'CANCELLED'}

class DELETE_OT_unlocked_shapekeys(Operator):
    """Delete all unlocked shapekeys except basis
    
    This operator removes all shapekeys that are not locked and not the basis key.
    It performs the deletion in a single operation for better performance.
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
            
            # Count locked shapekeys (excluding basis)
            locked_count = len([key for key in shape_keys.key_blocks[1:] 
                             if key.lock_shape])
            
            # Get all shape keys that should be deleted (not basis, not locked)
            keys_to_remove = [key for key in shape_keys.key_blocks[1:] 
                            if not key.lock_shape]
            
            deleted_count = len(keys_to_remove)
            
            # Remove all collected keys at once
            for key in keys_to_remove:
                obj.shape_key_remove(key)
            
            # Report the counts
            self.report({'INFO'}, f"Deleted {deleted_count} shapekeys except {locked_count} locked")
            
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Failed to delete shapekeys: {str(e)}")
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
        col.operator("object.delete_unlocked_shapekeys", icon='REMOVE')
        
        # Separator between button groups
        layout.separator()
        
        # Advanced Operations buttons
        box = layout.box()
        col = box.column(align=True)
        col.operator("object.add_shapekey_mirror", icon='ARROW_LEFTRIGHT')
        col.operator("object.add_shapekey_split_lr", icon='MOD_MIRROR')
        col.operator("object.add_shapekey_smart_split_mouth_lr", icon='MOD_MIRROR')
        
        # Add version information
        layout.separator()
        box = layout.box()
        col = box.column()
        col.scale_y = 0.8
        col.label(text="Version: 1.2.0")
        col.label(text="Last Updated: 2025/1/15")
        col.label(text="Blender: 2.80 → 4.32")

def register():
    """Register all classes"""
    bpy.utils.register_class(ADD_OT_shapekey_below)
    bpy.utils.register_class(ADD_OT_shapekey_from_mix_below)
    bpy.utils.register_class(ADD_OT_shapekey_split_lr)
    bpy.utils.register_class(ADD_OT_shapekey_mirror)
    bpy.utils.register_class(ADD_OT_shapekey_smart_split_mouth_lr)
    bpy.utils.register_class(DELETE_OT_unlocked_shapekeys)
    bpy.utils.register_class(VIEW3D_PT_shapekey_tools)

def unregister():
    """Unregister all classes"""
    bpy.utils.unregister_class(VIEW3D_PT_shapekey_tools)
    bpy.utils.unregister_class(DELETE_OT_unlocked_shapekeys)
    bpy.utils.unregister_class(ADD_OT_shapekey_smart_split_mouth_lr)
    bpy.utils.unregister_class(ADD_OT_shapekey_mirror)
    bpy.utils.unregister_class(ADD_OT_shapekey_split_lr)
    bpy.utils.unregister_class(ADD_OT_shapekey_from_mix_below)
    bpy.utils.unregister_class(ADD_OT_shapekey_below)

if __name__ == "__main__":
    register() 
