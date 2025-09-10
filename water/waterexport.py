import bpy

from ..cwxml.water_quads import WaterData, WaterQuad, CalmingQuad, WaveQuad
from ..sollumz_properties import SollumType 
from .properties import WaterType, WaterQuadProperties, CalmingQuadProperties, WaveQuadProperties
from .utils import ensure_quad_data, is_valid_quad
from .. import logger


def set_corners(obj: bpy.types.Object, quad_xml: WaterQuad | CalmingQuad | WaveQuad):
    quad_xml.min_x = min((v.co.x for v in obj.data.vertices), default=0.0)
    quad_xml.max_x = max((v.co.x for v in obj.data.vertices), default=0.0)
    quad_xml.min_y = min((v.co.y for v in obj.data.vertices), default=0.0)
    quad_xml.max_y = max((v.co.y for v in obj.data.vertices), default=0.0)
    quad_xml.z = min((v.co.z for v in obj.data.vertices), default=0.0)


def water_from_obj(water_data_obj: bpy.types.Object) -> WaterData:
    water_data_xml = WaterData()

    for quads in water_data_obj.children:
        if quads.sollum_type == SollumType.WATER_QUADS:
            for water_quad_obj in quads.children:
                if not is_valid_quad(water_quad_obj):
                    logger.warning(f"Skipping invalid quad {water_quad_obj.name}")
                    continue

                water_quad_xml = WaterQuad()
                water_quad_props: WaterQuadProperties = water_quad_obj.water_quad_properties
                set_corners(water_quad_obj, water_quad_xml)

                water_quad_xml.type = WaterType[water_quad_props.type].value
                water_quad_xml.is_invisible = water_quad_props.is_invisible
                water_quad_xml.has_limited_depth = water_quad_props.has_limited_depth
                water_quad_xml.a1 = water_quad_props.a1
                water_quad_xml.a2 = water_quad_props.a2
                water_quad_xml.a3 = water_quad_props.a3
                water_quad_xml.a4 = water_quad_props.a4
                water_quad_xml.no_stencil = water_quad_props.no_stencil
                water_data_xml.water_quads.append(water_quad_xml)

        if quads.sollum_type == SollumType.CALMING_QUADS:
            for calming_quad_obj in quads.children:
                if not is_valid_quad(calming_quad_obj):
                    logger.warning(f"Skipping invalid quad {calming_quad_obj.name}")
                    continue

                calming_quad_xml = CalmingQuad()
                calming_quad_props: CalmingQuadProperties = calming_quad_obj.calming_quad_properties
                set_corners(calming_quad_obj, calming_quad_xml)

                calming_quad_xml.f_dampening = calming_quad_props.f_dampening
                water_data_xml.calming_quads.append(calming_quad_xml)

        if quads.sollum_type == SollumType.WAVE_QUADS:
            for wave_quad_obj in quads.children:
                if not is_valid_quad(wave_quad_obj):
                    logger.warning(f"Skipping invalid quad {wave_quad_obj.name}")
                    continue

                wave_quad_xml = WaveQuad()
                wave_quad_props: WaveQuadProperties = wave_quad_obj.wave_quad_properties
                set_corners(wave_quad_obj, wave_quad_xml)

                wave_quad_xml.amplitude = wave_quad_props.amplitude
                wave_quad_xml.x_direction = wave_quad_props.x_direction
                wave_quad_xml.y_direction = wave_quad_props.y_direction
                water_data_xml.wave_quads.append(wave_quad_xml)

    return water_data_xml

def export_water(obj: bpy.types.Object, filepath: str) -> bool:
    water = water_from_obj(obj)
    water.write_xml(filepath)
    return True
