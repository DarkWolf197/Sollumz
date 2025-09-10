import bpy
from ..sollumz_properties import SollumType
from ..sollumz_ui import SOLLUMZ_PT_OBJECT_PANEL, SOLLUMZ_PT_MAT_PANEL
from .properties import WaterQuadProperties, CalmingQuadProperties, WaveQuadProperties

class SOLLUMZ_PT_WATER_PROPERTIES_PANEL(bpy.types.Panel):
    bl_label = "Water Quad Properties"
    bl_idname = "SOLLUMZ_PT_WATER_PROPERTIES_PANEL"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_options = {"HIDE_HEADER"}
    bl_parent_id = SOLLUMZ_PT_OBJECT_PANEL.bl_idname

    def draw(self, context):
        aobj = context.active_object
        self.layout.use_property_split = True
        self.layout.use_property_decorate = False

        if aobj.sollum_type == SollumType.WATER_DATA:
            self.layout.operator("sollumz.fix_water_quads", text="Fix Water Quads")
            self.layout.label(text=f"Degenerate Water Quads: {context.scene.degenerate_water_quads}")

        if aobj.sollum_type == SollumType.WATER_QUAD:
            for prop in WaterQuadProperties.__annotations__:
                self.layout.prop(aobj.water_quad_properties, prop)

        elif aobj.sollum_type == SollumType.CALMING_QUAD:
            for prop in CalmingQuadProperties.__annotations__:
                self.layout.prop(aobj.calming_quad_properties, prop)

        elif aobj.sollum_type == SollumType.WAVE_QUAD:
            for prop in WaveQuadProperties.__annotations__:
                self.layout.prop(aobj.wave_quad_properties, prop)
