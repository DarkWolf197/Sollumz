import bpy
from ..cwxml.nodepath import *
from ..sollumz_properties import SOLLUMZ_UI_NAMES, SollumType


def node_from_obj(obj):

    node = Node()
    node.area_id = obj.node_properties.area_id
    node.node_id = obj.node_properties.node_id
    node.streetname = obj.node_properties.streetname
    node.position = obj.location
    node.flags_0 = obj.node_properties.flags_0
    node.flags_1 = obj.node_properties.flags_1
    node.flags_2 = obj.node_properties.flags_2
    node.flags_3 = obj.node_properties.flags_3
    node.flags_4 = obj.node_properties.flags_4
    node.flags_5 = obj.node_properties.flags_5


def ynd_from_object(obj):
    ynd = NodePath()

    obj.node_path_properties.vehicle_node_count = ynd.vehicle_node_count
    obj.node_path_properties.ped_node_count = ynd.ped_node_count

    for child in obj.children:
        if child.node_properties.junction_found == True:
            pass
        else:
            ynd.nodes.append(node_from_obj(child))
        

    return ynd


def export_ynd(obj: bpy.types.Object, filepath: str) -> bool:
    ynd = ynd_from_object(obj)
    ynd.write_xml(filepath)
    return True