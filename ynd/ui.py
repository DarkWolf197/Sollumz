import bpy
from ..sollumz_properties import SollumType
from ..sollumz_ui import FlagsPanel, BasicListHelper, draw_list_with_add_remove
from ..tabbed_panels import TabbedPanelHelper, TabPanel
from ..tools.utils import get_list_item

class SOLLUMZ_UL_LINKS_LIST(BasicListHelper, bpy.types.UIList):
    bl_idname = "SOLLUMZ_UL_LINKS_LIST"
    item_icon = "DECORATE_LINKED"

class SOLLUMZ_PT_YND_TOOL_PANEL(bpy.types.Panel):
    bl_label = "Traffic Editor"
    bl_idname = "SOLLUMZ_PT_YND_TOOL_PANEL"
    bl_category = "Sollumz Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}
    bl_order = 7

    def draw_header(self, context):
        self.layout.label(text="", icon="SNAP_MIDPOINT")

    def draw(self, context):
        layout = self.layout
        obj = context.active_object

        if obj:
            if obj.sollum_type == SollumType.NODE_DICTIONARY:
                box = layout.box()
                box.label(text="Dictionary Properties")
                box.label(text=f"Veh Nodes: {obj.node_path_properties.vehicle_node_count}")
                box.label(text=f"Ped Nodes: {obj.node_path_properties.ped_node_count}")
                
            elif obj.sollum_type == SollumType.TRAFFIC_NODE:
                box = layout.box()
                box.label(text="Node Properties")
                box.prop(obj.node_properties, "area_id")
                box.prop(obj.node_properties, "node_id")
                box.prop(obj.node_properties, "streetname")

            else:
                layout.label(text="Object needs to be Node or Node Dictionary")
        else:
            layout.label(text="No Node or Junction Selected")


class YndToolChildPanel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = SOLLUMZ_PT_YND_TOOL_PANEL.bl_idname
    bl_category = SOLLUMZ_PT_YND_TOOL_PANEL.bl_category

class SOLLUMZ_PT_NODE_FLAGS_PANEL(YndToolChildPanel, FlagsPanel, bpy.types.Panel):
    bl_idname = "SOLLUMZ_PT_NODE_FLAGS_PANEL"
    icon = "BOOKMARKS"
    bl_order = 0

    @classmethod
    def poll(self, context):
        aobj = context.active_object
        return aobj is not None and aobj.sollum_type == SollumType.TRAFFIC_NODE

    def get_flags(self, context):
        selected_node = context.view_layer.objects.active
        return selected_node.node_properties.flags


class SOLLUMZ_PT_NODE_LINKS_PANEL(YndToolChildPanel, TabbedPanelHelper, bpy.types.Panel):
    bl_label = "Links"
    bl_idname = "SOLLUMZ_PT_NODE_LINKS_PANEL"
    bl_options = {"DEFAULT_CLOSED"}
    bl_order = 1

    @classmethod
    def poll(self, context):
        aobj = context.active_object
        return aobj is not None and aobj.sollum_type == SollumType.TRAFFIC_NODE

    def draw(self, context):
        layout = self.layout
        active_node = context.active_object.node_properties

        draw_list_with_add_remove(layout, "sollumz.createlink", "sollumz.deletelink",
            SOLLUMZ_UL_LINKS_LIST.bl_idname, "", active_node, "links", active_node, "link_index")
        
        layout.prop(active_node.links[active_node.link_index], "to_area_id")
        layout.prop(active_node.links[active_node.link_index], "to_node_id")
        layout.prop(active_node.links[active_node.link_index], "length")

class NodeLinksChildTabPanel(TabPanel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = SOLLUMZ_PT_NODE_LINKS_PANEL.bl_idname
    bl_category = SOLLUMZ_PT_NODE_LINKS_PANEL.bl_category
    
    parent_tab_panel = SOLLUMZ_PT_NODE_LINKS_PANEL


class SOLLUMZ_PT_LINK_FLAGS_PANEL(NodeLinksChildTabPanel, FlagsPanel, bpy.types.Panel):
    bl_idname = "SOLLUMZ_PT_LINK_FLAGS_PANEL"
    icon = "BOOKMARKS"

    @classmethod
    def poll(self, context):
        aobj = context.active_object
        return aobj is not None and aobj.sollum_type == SollumType.TRAFFIC_NODE

    def get_flags(self, context):
        active_node = context.active_object.node_properties
        return get_list_item(active_node.links, active_node.link_index).flags
    

class SOLLUMZ_PT_JUNCTIONS_PANEL(YndToolChildPanel, bpy.types.Panel):
    bl_label = "Junctions"
    bl_idname = "SOLLUMZ_PT_JUNCTIONS_PANEL"
    bl_options = {"DEFAULT_CLOSED"}
    bl_order = 2

    @classmethod
    def poll(self, context):
        aobj = context.active_object

        return (aobj is not None and aobj.sollum_type == SollumType.TRAFFIC_NODE) and aobj.node_properties.flags.has_junction

    def draw(self, context):
        layout = self.layout
        active_node = context.active_object.node_properties
        box = layout.box()

        box.prop(active_node.junctionref, "area_id")
        box.prop(active_node.junctionref, "node_id")
        box.prop(active_node.junctionref, "junction_id")
        box.prop(active_node.junctionref, "unk_0")
        
        box = layout.box()
        box.prop(active_node.junction, "position_x")
        box.prop(active_node.junction, "position_y")
        box.prop(active_node.junction, "min_z")
        box.prop(active_node.junction, "max_z")
        box.prop(active_node.junction, "size_x")
        box.prop(active_node.junction, "size_y")
        box.prop(active_node.junction, "heightmap")