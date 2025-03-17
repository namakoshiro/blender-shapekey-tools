bl_info = {
    "name": "Shapekey Tools",
    "author": "namakoshiro",
    "version": (1, 3, 1),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Shapekey",
    "description": "This is a Blender addon to manage shapekeys",
    "warning": "",
    "wiki_url": "https://github.com/namakoshiro/blender-shapekey-tools",
    "doc_url": "https://github.com/namakoshiro/blender-shapekey-tools",
    "category": "Rigging",
    "support": "COMMUNITY"
}

import bpy

# Import from ui directory
from .ui import panels

# Import from utils directory
from .utils import install
from .utils import update

# Import from modules directory
from .modules import add_shapekey_below
from .modules import add_shapekey_from_mix
from .modules import delete_unlocked_shapekeys
from .modules import select_affected_vertices
from .modules import shapekey_mirror
from .modules import shapekey_split_lr
from .modules import smooth_split_mouth_lr

# Register
def register():
    add_shapekey_below.register()
    add_shapekey_from_mix.register()
    delete_unlocked_shapekeys.register()
    select_affected_vertices.register()
    shapekey_mirror.register()
    shapekey_split_lr.register()
    smooth_split_mouth_lr.register()
    
    panels.register()
    install.register()
    update.register()

# Unregister
def unregister():
    update.unregister()
    install.unregister()
    panels.unregister()
    
    smooth_split_mouth_lr.unregister()
    shapekey_split_lr.unregister()
    shapekey_mirror.unregister()
    select_affected_vertices.unregister()
    delete_unlocked_shapekeys.unregister()
    add_shapekey_from_mix.unregister()
    add_shapekey_below.unregister()

if __name__ == "__main__":
    register() 