import bpy

class SOLLUMZ_PT_WATER_TOOL_PANEL(bpy.types.Panel):
    bl_label = "Water Quads"
    bl_idname = "SOLLUMZ_PT_WATER_TOOL_PANEL"
    bl_category = "Sollumz Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}
    bl_order = 7

    def draw_header(self, context):
        self.layout.label(text="", icon="FCURVE_SNAPSHOT")
    
    def draw(self, context):
        layout = self.layout
        obj = context.active_object

        if obj and obj.sollum_type == "sollumz_water_quad":
            layout.prop(obj.water_quad_properties, "type")
            layout.prop(obj.water_quad_properties, "invisible")
            layout.prop(obj.water_quad_properties, "limited_depth")
            layout.prop(obj.water_quad_properties, "z")
            layout.prop(obj.water_quad_properties, "a1")
            layout.prop(obj.water_quad_properties, "a2")
            layout.prop(obj.water_quad_properties, "a3")
            layout.prop(obj.water_quad_properties, "a4")
            layout.prop(obj.water_quad_properties, "no_stencil")

        elif obj and obj.sollum_type == "sollumz_calming_quad":
            layout.prop(obj.calming_quad_properties, "dampening")

        elif obj and obj.sollum_type == "sollumz_wave_quad":
            layout.prop(obj.wave_quad_properties, "amplitude")
            layout.prop(obj.wave_quad_properties, "xdirection")
            layout.prop(obj.wave_quad_properties, "ydirection")

        else:
            layout.label(text="Select a Water Quad")