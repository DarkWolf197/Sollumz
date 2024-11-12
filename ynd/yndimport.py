import bpy
from ..cwxml.nodepath import YND
from ..sollumz_properties import SollumType
from ..tools.meshhelper import create_box
from .geonode import create_geonode
from .utils import find_node


def apply_node_properties(obj, node):
    obj.node_properties.area_id = node.area_id
    obj.node_properties.node_id = node.node_id
    obj.node_properties.streetname = node.streetname
    obj.location = node.position
    obj.node_properties.flags_0 = node.flags_0
    obj.node_properties.flags_1 = node.flags_1
    obj.node_properties.flags_2 = node.flags_2
    obj.node_properties.flags_3 = node.flags_3
    obj.node_properties.flags_4 = node.flags_4
    obj.node_properties.flags_5 = node.flags_5

    for i, link in enumerate(node.links):
        link_obj = obj.node_properties.links.add()
        apply_link_properties(link_obj, link)
        modifier = obj.modifiers.new(name="GeometryNodes", type='NODES')
        modifier.node_group = bpy.data.node_groups["StreetGeoNode"]
        modifier.name = f"Link {i + 1}"
        modifier["Socket_1"] = find_node(link_obj.to_area_id, link_obj.to_node_id)


def apply_link_properties(obj, link):
    obj.to_area_id = link.to_area_id
    obj.to_node_id = link.to_node_id
    obj.flags_0 = link.flags_0
    obj.flags_1 = link.flags_1
    obj.flags_2 = link.flags_2
    obj.length = link.length

def apply_junctionref_properties(obj, junctionref):
    obj.area_id = junctionref.area_id
    obj.node_id = junctionref.node_id
    obj.junction_id = junctionref.junction_id
    obj.unk_0 = junctionref.unk_0


def apply_junction_properties(obj, junction):
    obj.position = (0, 0, 0)
    obj.min_z = junction.min_z
    obj.max_z = junction.max_z
    obj.size_x = junction.size_x
    obj.size_y = junction.size_y
    obj.heightmap = junction.heightmap


def node_to_obj(parent_obj: bpy.types.Object, node):
    mesh = bpy.data.meshes.new("Node")
    node_obj = bpy.data.objects.new("PathNode", mesh)
    
    node_obj.sollum_type = SollumType.TRAFFIC_NODE

    create_box(mesh, size=0.5)

    node_obj.parent = parent_obj

    bpy.context.collection.objects.link(node_obj)
    bpy.context.view_layer.objects.active = node_obj

    apply_node_properties(node_obj, node)
    node_obj.name = f"PathNode {node_obj.node_properties.area_id}.{node_obj.node_properties.area_id}"

    return node_obj


def add_junction_to_node(junctionref, junction):
    for node_obj in bpy.context.scene.objects:
        if node_obj.sollum_type == SollumType.TRAFFIC_NODE and node_obj.node_properties.area_id == junctionref.area_id and node_obj.node_properties.node_id == junctionref.node_id:
            node_obj.node_properties.junction_found = True
            apply_junctionref_properties(node_obj.node_properties.junctionref, junctionref)
            apply_junction_properties(node_obj.node_properties.junction, junction)



def ynd_to_obj(ynd):
    ynd_obj = bpy.data.objects.new("NodeDictionary", None)
    ynd_obj.sollum_type = SollumType.NODE_DICTIONARY
    ynd_obj.lock_location = (True, True, True)
    ynd_obj.lock_rotation = (True, True, True)
    ynd_obj.lock_scale = (True, True, True)
    bpy.context.collection.objects.link(ynd_obj)
    bpy.context.view_layer.objects.active = ynd_obj

    ynd_obj.node_path_properties.vehicle_node_count = ynd.vehicle_node_count
    ynd_obj.node_path_properties.ped_node_count = ynd.ped_node_count

    create_geonode()
    for node in ynd.nodes:
        node_to_obj(ynd_obj, node)
    
    junctions = ynd.junctions
    for junctionref in ynd.junctionrefs:
        junction = junctions[junctionref.junction_id]
        add_junction_to_node(junctionref, junction)

    return ynd_obj


def import_ynd(filepath):
    ynd_xml = YND.from_xml_file(filepath)
    return ynd_to_obj(ynd_xml)