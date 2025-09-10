import bpy
from enum import IntEnum
from ..sollumz_properties import SollumType, SOLLUMZ_UI_NAMES

class WaterType(IntEnum):
    NORMAL = 0
    BOTTOM_RIGHT = 1
    BOTTOM_LEFT = 2
    TOP_RIGHT = 3
    TOP_LEFT = 4

WaterTypeItems = tuple((enum.name, label, desc, enum.value) for enum, label, desc in (
    (WaterType.NORMAL, "Normal", "Square"),
    (WaterType.BOTTOM_RIGHT, "Bottom Right", "Right triangle where the 90 degree angle is at maxX, minY"),
    (WaterType.BOTTOM_LEFT, "Bottom Left", "Right triangle where the 90 degree angle is at minX, minY"),
    (WaterType.TOP_RIGHT, "Top Right", "Right triangle where the 90 degree angle is at minX, maxY"),
    (WaterType.TOP_LEFT, "Top Left", "Right triangle where the 90 degree angle is at maxY, maxY"),
))


class WaterQuadProperties(bpy.types.PropertyGroup):
    type: bpy.props.EnumProperty(
        name="Angle Type",
        items=WaterTypeItems,
        default=WaterType.NORMAL.name,
    )
    is_invisible: bpy.props.BoolProperty(name="Is Invisible")
    has_limited_depth: bpy.props.BoolProperty(name="Has Limited Depth")
    a1: bpy.props.IntProperty(name="Alpha Corner 1")
    a2: bpy.props.IntProperty(name="Alpha Corner 2")
    a3: bpy.props.IntProperty(name="Alpha Corner 3")
    a4: bpy.props.IntProperty(name="Alpha Corner 4")
    no_stencil: bpy.props.BoolProperty(name="No Stencil")


class CalmingQuadProperties(bpy.types.PropertyGroup):
    f_dampening: bpy.props.FloatProperty(name="Dampening")


class WaveQuadProperties(bpy.types.PropertyGroup):
    amplitude: bpy.props.FloatProperty(name="Amplitude")
    x_direction: bpy.props.FloatProperty(name="X Direction")
    y_direction: bpy.props.FloatProperty(name="Y Direction")


def register():
    bpy.types.Scene.degenerate_water_quads = bpy.props.IntProperty(name="Degenerate Water Quads")
    bpy.types.Object.water_quad_properties = bpy.props.PointerProperty(type=WaterQuadProperties)
    bpy.types.Object.calming_quad_properties = bpy.props.PointerProperty(type=CalmingQuadProperties)
    bpy.types.Object.wave_quad_properties = bpy.props.PointerProperty(type=WaveQuadProperties)

def unregister():
    del bpy.types.Scene.degenerate_water_quads
    del bpy.types.Object.water_quad_properties
    del bpy.types.Object.calming_quad_properties
    del bpy.types.Object.wave_quad_properties
