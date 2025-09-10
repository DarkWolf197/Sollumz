import bpy
from ..sollumz_helper import SOLLUMZ_OT_base
from ..sollumz_properties import SollumType
from .utils import ensure_quad_data


class SOLLUMZ_OT_fix_water_quads(SOLLUMZ_OT_base, bpy.types.Operator):
    bl_idname = "sollumz.fix_water_quads"
    bl_label = f"Fix Water Quads"
    bl_description = "Fix the vertices of all water quads."

    def run(self, context):
        aobj = context.active_object
        context.scene.degenerate_water_quads = 0

        for child in aobj.children_recursive:
            if child.sollum_type in [SollumType.WATER_QUAD, SollumType.CALMING_QUAD, SollumType.WAVE_QUAD]:
                if not ensure_quad_data(child):
                    context.scene.degenerate_water_quads += 1
