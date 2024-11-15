import bpy
from ..cwxml.nodepath import *
from ..sollumz_properties import SOLLUMZ_UI_NAMES, SollumType

def read_node_flags0_values(obj):
    flags = 0
    flags |= (1 if obj.node_properties.flags.fill_group_1 else 0) << 0
    flags |= (1 if obj.node_properties.flags.fill_group_2 else 0) << 1
    flags |= (1 if obj.node_properties.flags.fill_group_3 else 0) << 2
    flags |= (1 if obj.node_properties.flags.offroad else 0) << 3
    flags |= (1 if obj.node_properties.flags.unused_4 else 0) << 4
    flags |= (1 if obj.node_properties.flags.nobigvehicles else 0) << 5
    flags |= (1 if obj.node_properties.flags.nogoright else 0) << 6
    flags |= (1 if obj.node_properties.flags.nogoleft else 0) << 7
    return flags

def read_node_flags1_values(obj):
    flags = 0
    flags |= (1 if obj.node_properties.flags.slip_lane else 0) << 0
    flags |= (1 if obj.node_properties.flags.indicate_keep_left else 0) << 1
    flags |= (1 if obj.node_properties.flags.indicate_keep_right else 0) << 2

    special_types = {
        'NONE': 0,
        'PARKING': 16,
        'PED_CROSSING': 80,
        'PED_ASSISTED': 112,
        'TRAFFIC_LIGHT': 120,
        'STOP_SIGN': 128,
        'CAUTION': 136,
        'PED_CROSSING_NOWAIT': 144,
        'EMERGENCY_VEHICLES': 152,
        'OFFROAD_JUNCTION': 160
    }
    special_type = special_types.get(obj.node_properties.flags.special_type, 0)
    flags |= special_type
    return flags

def read_node_flags2_values(obj):
    flags = 0
    flags |= (1 if obj.node_properties.flags.no_gps else 0) << 0
    flags |= (1 if obj.node_properties.flags.unused_5 else 0) << 1
    flags |= (1 if obj.node_properties.flags.junction else 0) << 2
    flags |= (1 if obj.node_properties.flags.unused_6 else 0) << 3
    flags |= (1 if obj.node_properties.flags.switched_off_original else 0) << 4
    flags |= (1 if obj.node_properties.flags.water_node else 0) << 5
    flags |= (1 if obj.node_properties.flags.highway_bridge else 0) << 6
    flags |= (1 if obj.node_properties.flags.switched_off else 0) << 7
    return flags

def read_node_flags3_values(obj):
    flags = 0
    flags |= (1 if obj.node_properties.flags.tunnel else 0)
    flags |= obj.node_properties.flags.heuretic << 1
    return flags

def read_node_flags4_values(obj):
    flags = 0
    flags |= obj.node_properties.flags.density & 0xF
    flags |= (obj.node_properties.flags.deadness & 0xF) << 4
    flags |= (1 if obj.node_properties.flags.left_turn_only else 0) << 7
    return flags

def read_node_flags5_values(obj):
    flags = 0
    flags |= (1 if obj.node_properties.flags.has_heightmap else 0)

    speed_levels = ['SLOW', 'NORMAL', 'FAST', 'FASTER']
    index = min(speed_levels.index(obj.node_properties.flags.speed), len(speed_levels) - 1)
    flags |= index << 1
    return flags


def read_link_flags0_values(obj):
    flags = 0
    flags |= (1 if obj.flags.gps_both_ways else 0) << 0
    flags |= (1 if obj.flags.block_if_no_lanes else 0) << 1
    flags |= obj.flags.tilt << 2
    flags |= obj.flags.tilt_falloff << 5
    return flags


def read_link_flags1_values(obj):
    flags = 0
    flags |= (1 if obj.flags.tilt_falloff_2 else 0) << 0
    flags |= (1 if obj.flags.narrow_road else 0) << 1
    flags |= (1 if obj.flags.leads_to_dead_end else 0) << 2
    flags |= (1 if obj.flags.leads_from_dead_end else 0) << 3
    flags |= (1 if obj.flags.negative_offset else 0) << 7
    flags |= obj.flags.width << 4
    return flags


def read_link_flags2_values(obj):
    flags = 0
    flags |= (1 if obj.flags.dont_use_for_navigation else 0) << 0
    flags |= (1 if obj.flags.shortcut else 0) << 1
    flags |= obj.flags.bwd_lanes << 2
    flags |= obj.flags.fwd_lanes << 5
    return flags


def node_from_obj(obj):

    node = Node()
    node.area_id = obj.node_properties.area_id
    node.node_id = obj.node_properties.node_id
    node.streetname = obj.node_properties.streetname
    node.position = obj.location
    node.flags_0 = read_node_flags0_values(obj)
    node.flags_1 = read_node_flags1_values(obj)
    node.flags_2 = read_node_flags2_values(obj)
    node.flags_3 = read_node_flags3_values(obj)
    node.flags_4 = read_node_flags4_values(obj)
    node.flags_5 = read_node_flags5_values(obj)
    node.links = link_from_obj(obj)

    return node


def link_from_obj(obj):
    links = []
    for link_data in obj.node_properties.links:
        link = Link()
        link.to_area_id = link_data.to_area_id
        link.to_node_id = link_data.to_node_id
        link.flags_0 = read_link_flags0_values(link_data)
        link.flags_1 = read_link_flags1_values(link_data)
        link.flags_2 = read_link_flags2_values(link_data)
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
        ynd.nodes.append(node_from_obj(child))
        ynd.junctions.append(junction_from_obj(child))
        ynd.junctionrefs.append(junctionref_from_obj(child))
        

    return ynd


def export_ynd(obj: bpy.types.Object, filepath: str) -> bool:
    ynd = ynd_from_object(obj)
    ynd.write_xml(filepath)
    return True