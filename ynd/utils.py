import bpy
from ..sollumz_properties import SollumType

def find_node_obj(area_id, node_id):
    for obj in bpy.data.objects:
        if (obj.sollum_type == SollumType.NODE and
            obj.node_properties.area_id == area_id and
            obj.node_properties.node_id == node_id
            ):
            return obj