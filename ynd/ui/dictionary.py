import bpy
from ...sollumz_properties import SollumType
from ...sollumz_ui import SOLLUMZ_PT_OBJECT_PANEL
from ..properties import NodeDictionaryProperties

class SOLLUMZ_PT_NODE_DICTIONARY_PANEL(bpy.types.Panel):
    bl_label = "Node Dictionary Properties"
    bl_idname = "SOLLUMZ_PT_NODE_DICTIONARY_PANEL"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_parent_id = SOLLUMZ_PT_OBJECT_PANEL.bl_idname

    @classmethod
    def poll(cls, context):
        obj = context.active_object

        if obj is None:
            return False

        return obj.sollum_type == SollumType.NODE_DICTIONARY

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        ynd_props: NodeDictionaryProperties = obj.node_dictionary_properties

        layout.label(text=f"Ped Node Count: {ynd_props.ped_node_count}")
        layout.label(text=f"Vehicle Node Count: {ynd_props.vehicle_node_count}")

        grid = layout.grid_flow(columns=2, even_columns=True, even_rows=True)
        grid.use_property_split = True
        grid.use_property_decorate = False

        grid.prop(ynd_props, "x")
        grid.prop(ynd_props, "y")
