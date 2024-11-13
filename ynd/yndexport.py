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
    node.links = link_from_obj(obj)

    return node


def link_from_obj(obj):
    links = []
    for link_data in obj.node_properties.links:
        link = Link()
        link.to_area_id = link_data.to_area_id
        link.to_node_id = link_data.to_node_id
        link.flags_0 = link_data.flags_0
        link.flags_1 = link_data.flags_1
        link.flags_2 = link_data.flags_2
        link.length = link_data.length
        links.append(link)
    return links



def junction_from_obj(obj):
    
    junction = Junction()
    junction.position = obj.node_properties.junction.position
    junction.min_z = obj.node_properties.junction.min_z
    junction.max_z = obj.node_properties.junction.max_z
    junction.size_x =  obj.node_properties.junction.size_x
    junction.size_y = obj.node_properties.junction.size_y
    junction.heightmap = obj.node_properties.junction.heightmap

    return junction


def junctionref_from_obj(obj):

    junctionref = JunctionRef()
    junctionref.area_id = obj.node_properties.junctionref.area_id
    junctionref.node_id = obj.node_properties.junctionref.node_id
    junctionref.junction_id = obj.node_properties.junctionref.junction_id
    junctionref.unk_0 = obj.node_properties.junctionref.unk_0

    return junctionref

def ynd_from_object(obj):
    ynd = NodePath()

    ynd.vehicle_node_count = obj.node_path_properties.vehicle_node_count
    ynd.ped_node_count = obj.node_path_properties.ped_node_count

    for child in obj.children:
        if child.node_properties.junction_found == True:
            ynd.junctions.append(junction_from_obj(child))
            ynd.junctionrefs.append(junctionref_from_obj(child))

        ynd.nodes.append(node_from_obj(child))
        

    return ynd


def export_ynd(obj: bpy.types.Object, filepath: str) -> bool:
    ynd = ynd_from_object(obj)
    ynd.write_xml(filepath)
    return True