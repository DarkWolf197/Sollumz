import bpy
from ..cwxml.nodepath import YND
from ..tools.meshhelper import (
    create_box,
    create_sphere,
    create_cylinder,
    create_capsule,
    create_disc,
)


def apply_node_properties(obj, node):
    obj.node_properties.area_id = node.area_id
    obj.node_properties.node_id = node.node_id
    obj.node_properties.streetname = node.streetname
    obj.location = node.position
    obj.node_properties.flags_0 = node.flags_0
    obj.node_properties.flags_1 = node.flags_1
    obj.node_properties.flags_2 = node.flags_2
    obj.node_properties.flags_3 = node.flags_4
    obj.node_properties.flags_4 = node.flags_4
    obj.node_properties.flags_5 = node.flags_5
    #obj.node_properties.links = node.links

def apply_link_properties(obj, link):
    obj.link_properties.to_area_id = link.to_area_id
    obj.link_properties.to_node_id = link.to_node_id
    obj.link_properties.flags_0 = link.flags_0
    obj.link_properties.flags_1 = link.flags_1
    obj.link_properties.flags_2 = link.flags_2
    obj.link_properties.length = link.length

def apply_junctionref_properties(obj, junctionref):
    obj.junctionref_properties.area_id = junctionref.area_id
    obj.junctionref_properties.node_id = junctionref.node_id
    obj.junctionref_properties.junction_id = junctionref.junction_id
    obj.junctionref_properties.unk_0 = junctionref.unk_0

def apply_junction_properties(obj, junction):
    obj.location = (junction.position[0], junction.position[1], 0)
    obj.junction_properties.min_z = junction.min_z
    obj.junction_properties.max_z = junction.max_z
    obj.junction_properties.size_x = junction.size_x
    obj.junction_properties.size_y = junction.size_y
    obj.junction_properties.heightmap = junction.heightmap


def node_to_obj(parent_obj: bpy.types.Object, node):
    mesh = bpy.data.meshes.new("Node")
    node_obj = bpy.data.objects.new("Node", mesh)
    
    create_box(mesh, size=0.8)

    node_obj.parent = parent_obj

    bpy.context.collection.objects.link(node_obj)
    bpy.context.view_layer.objects.active = node_obj

    apply_node_properties(node_obj, node)

    return node_obj


def junction_to_obj(parent_obj: bpy.types.Object, node):
    junction_obj = bpy.data.objects.new("Junction", None)
    junction_obj.parent = parent_obj
    
    bpy.context.collection.objects.link(junction_obj)
    bpy.context.view_layer.objects.active = junction_obj

    apply_junction_properties(junction_obj, node)

    return junction_obj


def junctionref_to_obj(parent_obj: bpy.types.Object, node):
    junctionref_obj = bpy.data.objects.new("JunctionRef", None)
    junctionref_obj.parent = parent_obj
    
    bpy.context.collection.objects.link(junctionref_obj)
    bpy.context.view_layer.objects.active = junctionref_obj

    apply_junctionref_properties(junctionref_obj, node)

    return junctionref_obj


def ynd_to_obj(ynd):
    ynd_obj = bpy.data.objects.new("NodeDictionary", None)
    ynd_obj.lock_location = (True, True, True)
    ynd_obj.lock_rotation = (True, True, True)
    ynd_obj.lock_scale = (True, True, True)
    
    bpy.context.collection.objects.link(ynd_obj)
    bpy.context.view_layer.objects.active = ynd_obj

    ynd_obj.node_path_properties.vehicle_node_count = ynd.vehicle_node_count
    ynd_obj.node_path_properties.ped_node_count = ynd.ped_node_count

    for node in ynd.nodes:
        node_to_obj(ynd_obj, node)

    for junction in ynd.junctions:
        junction_to_obj(ynd_obj, junction)

    for junctionref in ynd.junctionrefs: 
        junctionref_to_obj(ynd_obj, junctionref)

    return ynd_obj


def import_ynd(filepath):
    ynd_xml = YND.from_xml_file(filepath)
    return ynd_to_obj(ynd_xml)