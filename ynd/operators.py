import bpy
from .properties import NodeProperties, LinkProperties
from ..tools.utils import get_list_item


class SOLLUMZ_OT_create_node_link(bpy.types.Operator):
    bl_idname = "sollumz.create_node_link"
    bl_options = {"UNDO"}
    bl_label = "Add Link"

    def execute(self, context):
        aobj = context.active_object.node_properties
        item: LinkProperties = aobj.links.add()

        item.name = f"{aobj.area_id}, 0, 0"

        return {"FINISHED"}


class SOLLUMZ_OT_delete_node_link(bpy.types.Operator):
    bl_idname = "sollumz.delete_node_link"
    bl_options = {"UNDO"}
    bl_label = "Delete Link"

    def execute(self, context):
        aobj = context.active_object
        node_props: NodeProperties = aobj.node_properties

        if not get_list_item(node_props.links, node_props.link_index):
            return

        aobj.links.remove(node_props.link_index)
        node_props.link_index = max(node_props.link_index - 1, 0)

        return {"FINISHED"}