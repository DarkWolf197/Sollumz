import bpy
from ..sollumz_properties import SollumType

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
