import bpy
from mathutils import Matrix
import bmesh
from typing import Union

from ..cwxml.water_quads import WATER, WaterData, WaterQuad, CalmingQuad, WaveQuad
from ..sollumz_properties import SollumType, SOLLUMZ_UI_NAMES 
from ..tools.blenderhelper import create_blender_object, create_empty_object, parent_objs
from .utils import create_quad_materials
from .. import logger
from .properties import WaterType, WaterQuadProperties, CalmingQuadProperties, WaveQuadProperties

def create_plane(mesh: bpy.types.Mesh, water_quad_xml: WaterQuad) -> bpy.types.Mesh:
    """Create a quad mesh from given bounds."""
    bm = bmesh.new()

    min_x = water_quad_xml.min_x
    max_x = water_quad_xml.max_x
    min_y = water_quad_xml.min_y
    max_y = water_quad_xml.max_y
    z = water_quad_xml.z or 0.0

    v1 = bm.verts.new((min_x, min_y, z)) 
    v2 = bm.verts.new((max_x, min_y, z))
    v3 = bm.verts.new((max_x, max_y, z))
    v4 = bm.verts.new((min_x, max_y, z))
    
    bm.faces.new([v1, v2, v3, v4])
    bm.to_mesh(mesh)
    bm.free()

    return mesh


def water_to_obj(water_xml: WaterData, filename: str) -> bpy.types.Object:
    water_data_obj = create_empty_object(SollumType.WATER_DATA, filename)
    water_quads_obj = create_empty_object(SollumType.WATER_QUADS)
    calming_quads_obj = create_empty_object(SollumType.CALMING_QUADS)
    wave_quads_obj = create_empty_object(SollumType.WAVE_QUADS)
    parent_objs([water_quads_obj, calming_quads_obj, wave_quads_obj], water_data_obj)
    water_mat, calming_mat, wave_mat = create_quad_materials()

    for water_quad_xml in water_xml.water_quads:
        water_quad_obj = create_blender_object(SollumType.WATER_QUAD)
        create_plane(water_quad_obj.data, water_quad_xml)
        water_quad_obj.parent = water_quads_obj
        water_quad_obj.data.materials.append(water_mat)

        water_quad_props: WaterQuadProperties = water_quad_obj.water_quad_properties
        water_quad_props.type = WaterType(water_quad_xml.type).name
        water_quad_props.is_invisible = water_quad_xml.is_invisible
        water_quad_props.has_limited_depth = water_quad_xml.has_limited_depth
        water_quad_props.a1 = water_quad_xml.a1
        water_quad_props.a2 = water_quad_xml.a2
        water_quad_props.a3 = water_quad_xml.a3
        water_quad_props.a4 = water_quad_xml.a4
        water_quad_props.no_stencil = water_quad_xml.no_stencil

    for calming_quad_xml in water_xml.calming_quads:
        calming_quad_obj = create_blender_object(SollumType.CALMING_QUAD)
        create_plane(calming_quad_obj.data, calming_quad_xml)
        calming_quad_obj.parent = calming_quads_obj
        calming_quad_obj.data.materials.append(calming_mat)

        calming_quad_props: CalmingQuadProperties = calming_quad_obj.calming_quad_properties
        calming_quad_props.f_dampening = calming_quad_xml.f_dampening

    for wave_quad_xml in water_xml.wave_quads:
        wave_quad_obj = create_blender_object(SollumType.WAVE_QUAD)
        create_plane(wave_quad_obj.data, wave_quad_xml)
        wave_quad_obj.parent = wave_quads_obj
        wave_quad_obj.data.materials.append(wave_mat)

        wave_quad_props: WaveQuadProperties = wave_quad_obj.wave_quad_properties
        wave_quad_props.amplitude = wave_quad_xml.amplitude
        wave_quad_props.x_direction = wave_quad_xml.x_direction
        wave_quad_props.y_direction = wave_quad_xml.y_direction


def import_water(filepath: str):
    water_xml: WaterData = WATER.from_xml_file(filepath)
    filename = filepath.split("\\")[-1].partition(".")[0]
    found = False
    for obj in bpy.context.scene.objects:
        if obj.name == filename:
            logger.error(
                f"{filename} is already existing in the scene. Aborting.")
            found = True
            break
    if not found:
        water_to_obj(water_xml, filename)
