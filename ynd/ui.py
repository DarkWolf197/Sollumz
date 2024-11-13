import bpy
from ..sollumz_properties import SollumType
from ..sollumz_ui import FlagsPanel

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
            if obj.sollum_type == SollumType.TRAFFIC_NODE:
                box = layout.box()
                box.label(text="Node Properties")
                box.label(text=f"Area ID: {obj.node_properties.area_id}")
                box.label(text=f"Node ID: {obj.node_properties.node_id}")
                box.label(text=f"Street Name: {obj.node_properties.streetname}")
                box.label(text=f"Flags 0: {obj.node_properties.flags_0}")
                box.label(text=f"Flags 1: {obj.node_properties.flags_1}")
                box.label(text=f"Flags 2: {obj.node_properties.flags_2}")
                box.label(text=f"Flags 3: {obj.node_properties.flags_3}")
                box.label(text=f"Flags 4: {obj.node_properties.flags_4}")
                box.label(text=f"Flags 5: {obj.node_properties.flags_5}")

                if obj.node_properties.junction_found:
                    box = layout.box()
                    box.label(text="Junction Refs")
                    box.label(text=f"  Junc ID: {obj.node_properties.junctionref.junction_id}")
                    box.label(text=f"  UNK_0: {obj.node_properties.junctionref.unk_0}")
                    box = layout.box()
                    box.label(text="Junction Properties")
                    box.label(text=f"Min Z: {obj.node_properties.junction.min_z}")
                    box.label(text=f"Max Z: {obj.node_properties.junction.max_z}")
                    box.label(text=f"Size X: {obj.node_properties.junction.size_x}")
                    box.label(text=f"Size Y: {obj.node_properties.junction.size_y}")
                    box.label(text=f"Heightmap: {obj.node_properties.junction.heightmap}")

                if obj.node_properties.links:
                    box = layout.box()
                    box.label(text="Link Properties")
                    for i, link in enumerate(obj.node_properties.links):
                        box.label(text=f"Link {i + 1}")
                        box.label(text=f"  To Area ID: {link.to_area_id}")
                        box.label(text=f"  To Node ID: {link.to_node_id}")
                        box.label(text=f"  Flags 0: {link.flags_0}")
                        box.label(text=f"  Flags 1: {link.flags_1}")
                        box.label(text=f"  Flags 2: {link.flags_2}")
                        box.label(text=f"  Length: {link.length}")

            elif obj.sollum_type == SollumType.NODE_DICTIONARY:
                box = layout.box()
                box.label(text="Dictionary Properties")
                box.label(text=f"Veh Nodes: {obj.node_path_properties.vehicle_node_count}")
                box.label(text=f"Ped Nodes: {obj.node_path_properties.ped_node_count}")
            else:
                layout.label(text="No Node or Junction Selected")
        else:
            layout.label(text="No Node or Junction Selected")

class YndToolChildPanel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = SOLLUMZ_PT_YND_TOOL_PANEL.bl_idname
    bl_category = SOLLUMZ_PT_YND_TOOL_PANEL.bl_category


class SOLLUMZ_PT_NODE_FLAGS_0_PANEL(YndToolChildPanel, bpy.types.Panel):
    bl_idname = "SOLLUMZ_PT_NODE_FLAGS_0_PANEL"
    bl_label = "Node Flags"
    icon = "BOOKMARKS"
    bl_order = 0

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        row = layout.row()
        col1 = row.column()
        col2 = row.column()
        col3 = row.column()

        flags0_box = col1.box()
        flags0_box.label(text="Flags0")
        flags0_box.prop(obj.node_properties.flags_0_toggle, "scripted")
        flags0_box.prop(obj.node_properties.flags_0_toggle, "gps_enabled")
        flags0_box.prop(obj.node_properties.flags_0_toggle, "unused_4")
        flags0_box.prop(obj.node_properties.flags_0_toggle, "offroad")
        flags0_box.prop(obj.node_properties.flags_0_toggle, "unused_16")
        flags0_box.prop(obj.node_properties.flags_0_toggle, "nobigvehicles")
        flags0_box.prop(obj.node_properties.flags_0_toggle, "nogoright")
        flags0_box.prop(obj.node_properties.flags_0_toggle, "nogoleft")


        flags1_box = col2.box()
        flags1_box.label(text="Flags1")
        flags1_box.prop(obj.node_properties.flags_1_toggle, "slip_lane")
        flags1_box.prop(obj.node_properties.flags_1_toggle, "indicate_keep_left")
        flags1_box.prop(obj.node_properties.flags_1_toggle, "indicate_keep_right")
        flags1_box.prop(obj.node_properties.flags_1_toggle, "special_type", text="")


        flags2_box = col3.box()
        flags2_box.label(text="Flags2")
        flags2_box.prop(obj.node_properties.flags_2_toggle, "no_gps")
        flags2_box.prop(obj.node_properties.flags_2_toggle, "unused_2")
        flags2_box.prop(obj.node_properties.flags_2_toggle, "junction")
        flags2_box.prop(obj.node_properties.flags_2_toggle, "unused_8")
        flags2_box.prop(obj.node_properties.flags_2_toggle, "disabled_1")
        flags2_box.prop(obj.node_properties.flags_2_toggle, "water_boats")
        flags2_box.prop(obj.node_properties.flags_2_toggle, "freeway")
        flags2_box.prop(obj.node_properties.flags_2_toggle, "disabled_2")