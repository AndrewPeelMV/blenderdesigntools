
'''
Created by Andrew Peel

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {
    "name": "Room Designer",
    "author": "Andrew Peel",
    "version": (1, 0, 0),
    "blender": (2, 7, 0),
    "location": "Tools Shelf",
    "description": "This add-on allows you to quickly create rooms.",
    "warning": "",
    "wiki_url": "",
    "category": "Design Tools"
}

import bpy
from . import room_designer

def clear_blender_panels():
    if hasattr(bpy.types, 'VIEW3D_PT_grease_pencil'):
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_grease_pencil)
    if hasattr(bpy.types, 'VIEW3D_PT_grease_pencil_palettecolor'):
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_grease_pencil_palettecolor)
    if hasattr(bpy.types, 'VIEW3D_PT_view3d_properties'):
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_view3d_properties)
    if hasattr(bpy.types, 'VIEW3D_PT_view3d_cursor'):
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_view3d_cursor)
    if hasattr(bpy.types, 'VIEW3D_PT_view3d_name'):
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_view3d_name)
    if hasattr(bpy.types, 'VIEW3D_PT_view3d_display'):
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_view3d_display)
    if hasattr(bpy.types, 'VIEW3D_PT_view3d_stereo'):
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_view3d_stereo)
    if hasattr(bpy.types, 'VIEW3D_PT_view3d_shading'):
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_view3d_shading)
    if hasattr(bpy.types, 'VIEW3D_PT_view3d_motion_tracking'):
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_view3d_motion_tracking)
    if hasattr(bpy.types, 'VIEW3D_PT_view3d_meshdisplay'):
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_view3d_meshdisplay)
    if hasattr(bpy.types, 'VIEW3D_PT_view3d_meshstatvis'):
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_view3d_meshstatvis)
    if hasattr(bpy.types, 'VIEW3D_PT_view3d_curvedisplay'):
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_view3d_curvedisplay)
    if hasattr(bpy.types, 'VIEW3D_PT_background_image'):
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_background_image)
    if hasattr(bpy.types, 'VIEW3D_PT_transform_orientations'):
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_transform_orientations)
    if hasattr(bpy.types, 'VIEW3D_PT_etch_a_ton'):
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_etch_a_ton)
    if hasattr(bpy.types, 'VIEW3D_PT_context_properties'):
        bpy.utils.unregister_class(bpy.types.VIEW3D_PT_context_properties)

def register():
    clear_blender_panels()
    room_designer.register()

def unregister():
    pass