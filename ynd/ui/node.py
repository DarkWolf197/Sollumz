import bpy
from ...tabbed_panels import TabbedPanelHelper, TabPanel
from ...sollumz_ui import SOLLUMZ_PT_OBJECT_PANEL
from ...sollumz_properties import SollumType
from ..properties import (
    NodeProperties,
    NodeFlags0, NodeFlags1, NodeFlags2, NodeFlags3, NodeFlags4, NodeFlags5,
    LinkFlags0, LinkFlags1, LinkFlags2
    )
from ...sollumz_ui import BasicListHelper, draw_list_with_add_remove
from ...tools.utils import get_list_item


class SOLLUMZ_UL_NODE_LINKS_LIST(BasicListHelper, bpy.types.UIList):
    bl_idname = "SOLLUMZ_UL_NODE_LINKS_LIST"
    item_icon = "DECORATE_LINKED"


class SOLLUMZ_PT_NODE_PROPERTIES_PANEL(bpy.types.Panel):
    bl_label = "Node Properties"
    bl_idname = "SOLLUMZ_PT_NODE_PROPERTIES_PANEL"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_parent_id = SOLLUMZ_PT_OBJECT_PANEL.bl_idname
    bl_order = 0

    @classmethod
    def poll(cls, context):
        obj = context.active_object

        if obj is None:
            return False

        return obj.sollum_type == SollumType.NODE

    def draw(self, context):
        layout = self.layout
        grid = layout.grid_flow(columns=2, even_columns=True, even_rows=True)
        grid.use_property_split = True
        grid.use_property_decorate = False

        obj = context.active_object
        node_props: NodeProperties = obj.node_properties

        grid.enabled = False
        grid.prop(node_props, "area_id")
        grid.prop(node_props, "node_id")
        layout.prop(node_props, "streetname")


class SOLLUMZ_PT_NODE_TABS_PANEL(TabbedPanelHelper, bpy.types.Panel):
    bl_label = "Node"
    bl_idname = "SOLLUMZ_PT_NODE_TABS_PANEL"
    bl_options = {"HIDE_HEADER"}
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_parent_id = SOLLUMZ_PT_OBJECT_PANEL.bl_idname

    default_tab = "SOLLUMZ_PT_NODE_LINKS_PANEL"

    bl_order = 1

    @classmethod
    def poll(cls, context):
        obj = context.active_object

        if obj is None:
            return False

        return obj.sollum_type == SollumType.NODE

    def draw_before(self, context: bpy.types.Context):
        self.layout.separator()


class NodeChildTabPanel(TabPanel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_options = {"HIDE_HEADER"}
    bl_parent_id = SOLLUMZ_PT_NODE_TABS_PANEL.bl_idname

    parent_tab_panel = SOLLUMZ_PT_NODE_TABS_PANEL


class SOLLUMZ_PT_NODE_LINKS_PANEL(NodeChildTabPanel, bpy.types.Panel):
    bl_label = "Links"
    bl_idname = "SOLLUMZ_PT_NODE_LINKS_PANEL"

    icon = "DECORATE_LINKED"

    bl_order = 0

    def draw(self, context):
        layout = self.layout
        aobj = context.active_object

        draw_list_with_add_remove(layout, "sollumz.create_node_link", "sollumz.delete_node_link",
                                  SOLLUMZ_UL_NODE_LINKS_LIST.bl_idname, "",
                                  aobj.node_properties, "links", aobj.node_properties, "link_index", rows=3)
        
        selected_link = get_list_item(aobj.node_properties.links, aobj.node_properties.link_index)

        if selected_link:
            row = layout.row()
            row.prop(selected_link, "linked_obj")
            row.operator("sollumz.goto_node", text="", icon="UV_SYNC_SELECT")

            grid = layout.grid_flow(columns=2, even_columns=True, even_rows=True)
            grid.use_property_split = True
            grid.use_property_decorate = False
            grid.enabled = False

            grid.prop(selected_link, "to_area_id")
            grid.prop(selected_link, "to_node_id")
            layout.label(text=f"Length: {selected_link.length}")
            

class SOLLUMZ_PT_NODE_LINKS_FLAGS_PANEL(bpy.types.Panel):
    bl_label = "Link Flags"
    bl_idname = "SOLLUMZ_PT_NODE_LINKS_FLAGS_PANEL"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_parent_id = SOLLUMZ_PT_NODE_LINKS_PANEL.bl_idname

    @classmethod
    def poll(cls, context):
        aobj = context.active_object
        return aobj and get_list_item(aobj.node_properties.links, aobj.node_properties.link_index)
    
    def draw(self, context):
        layout = self.layout
        aobj = context.active_object
        selected_link = get_list_item(aobj.node_properties.links, aobj.node_properties.link_index)

        flags0: LinkFlags0 = selected_link.flags0
        flags1: LinkFlags1 = selected_link.flags1
        flags2: LinkFlags2 = selected_link.flags2

        grid = layout.grid_flow(columns=2, even_columns=True, even_rows=True)
        grid.use_property_split = True
        grid.use_property_decorate = False

        grid.prop(flags0, "gps_both_ways")
        grid.prop(flags0, "block_if_no_lanes")
        grid.prop(flags0, "unknown_1")
        grid.prop(flags0, "unknown_2")

        grid.prop(flags1, "unused_1")
        grid.prop(flags1, "narrow_road")
        grid.prop(flags1, "dead_end")
        grid.prop(flags1, "dead_end_exit")
        grid.prop(flags1, "negative_offset")
        grid.prop(flags1, "offset")

        grid.prop(flags2, "dont_use_for_navigation")
        grid.prop(flags2, "shortcut")
        grid.prop(flags2, "back_lanes")
        grid.prop(flags2, "forward_lanes")


class SOLLUMZ_PT_NODE_FLAGS_PANEL(NodeChildTabPanel, bpy.types.Panel):
    bl_label = "Flags"
    bl_idname = "SOLLUMZ_PT_NODE_FLAGS_PANEL"

    icon = "BOOKMARKS"

    bl_order = 1

    def draw(self, context):
        layout = self.layout
 
        obj = context.active_object
        flags0: NodeFlags0 = obj.node_properties.flags0
        flags1: NodeFlags1 = obj.node_properties.flags1
        flags2: NodeFlags2 = obj.node_properties.flags2
        flags3: NodeFlags3 = obj.node_properties.flags3
        flags4: NodeFlags4 = obj.node_properties.flags4
        flags5: NodeFlags5 = obj.node_properties.flags5
 
        layout.prop(flags1, "special_type")
 
        grid = layout.grid_flow(columns=2, even_columns=True, even_rows=True)
        grid.use_property_split = True
        grid.use_property_decorate = False
 
        grid.prop(flags0, "scripted")
        grid.prop(flags0, "gps_enabled")
        grid.prop(flags0, "unused_4")
        grid.prop(flags0, "offroad")
        grid.prop(flags0, "unused_16")
        grid.prop(flags0, "no_big_vehicles")
        grid.prop(flags0, "cannot_go_right")
        grid.prop(flags0, "cannot_go_left")

        grid.prop(flags1, "slip_lane")
        grid.prop(flags1, "indicate_keep_left")
        grid.prop(flags1, "indicate_keep_right")
 
        grid.prop(flags2, "no_gps")
        grid.prop(flags2, "unused_2")
        grid.prop(flags2, "junction")
        grid.prop(flags2, "unused_8")
        grid.prop(flags2, "disabled_1")
        grid.prop(flags2, "water_boats")
        grid.prop(flags2, "Freeway")
        grid.prop(flags2, "disabled_2")
 
        grid.prop(flags3, "tunnel")
        grid.prop(flags3, "heuristic")
 
        grid.prop(flags4, "density")
        grid.prop(flags4, "deadendness")
        grid.prop(flags4, "left_turn_only")
 
        grid.prop(flags5, "has_junction_heightmap")
        grid.prop(flags5, "speed")

class SOLLUMZ_PT_NODE_TEST_PANEL(NodeChildTabPanel, bpy.types.Panel):
    bl_label = "Test"
    bl_idname = "SOLLUMZ_PT_NODE_TEST_PANEL"

    icon = "GRID"

    bl_order = 2

    def draw(self, context):
        aobj = context.active_object
        layout = self.layout

        is_junc = aobj.node_properties.flags2.junction
        has_hmap = aobj.node_properties.flags5.has_junction_heightmap
        if is_junc and has_hmap:

            grid = layout.grid_flow(columns=3, even_columns=True, even_rows=True)
            grid.use_property_split = True
            grid.use_property_decorate = False

            grid.prop(aobj.node_properties.junction, "max_z")
            grid.prop(aobj.node_properties.junction, "min_z")
            grid.prop(aobj.node_properties.junction, "pos_x")
            grid.prop(aobj.node_properties.junction, "pos_y")
            grid.prop(aobj.node_properties.junction, "size_x")
            grid.prop(aobj.node_properties.junction, "size_y")
            layout.label(text="To Generate Heightmap use CodeWalker", icon="ERROR")

        else:
            layout.label(text="Enable Junction Flags", icon="ERROR")
