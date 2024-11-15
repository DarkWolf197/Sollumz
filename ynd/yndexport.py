import bpy
from ..cwxml.nodepath import *
import mathutils

special_types = {
    0: 'NONE',
    16: 'PARKING',
    80: 'PED_CROSSING',
    112: 'PED_ASSISTED',
    120: 'TRAFFIC_LIGHT',
    128: 'STOP_SIGN',
    136: 'CAUTION',
    144: 'PED_CROSSING_NOWAIT',
    152: 'EMERGENCY_VEHICLES',
    160: 'OFFROAD_JUNCTION'}

speed_levels = ['SLOW', 'NORMAL', 'FAST', 'FASTER']

def get_node_flags(obj):
    flags0 = 0
    flags0 |= obj.fill_group_1 << 0
    flags0 |= obj.fill_group_2 << 1
    flags0 |= obj.fill_group_3 << 2
    flags0 |= obj.offroad << 3
    flags0 |= obj.unused_4 << 4
    flags0 |= obj.nobigvehicles << 5
    flags0 |= obj.nogoright << 6
    flags0 |= obj.nogoleft << 7

    flags1 = 0
    flags1 |= obj.slip_lane << 0
    flags1 |= obj.indicate_keep_left << 1
    flags1 |= obj.indicate_keep_right << 2
    flags1 |= list(special_types.keys())[list(special_types.values()).index(obj.special_type)]

    flags2 = 0
    flags2 |= obj.no_gps << 0
    flags2 |= obj.unused_5 << 1
    flags2 |= obj.junction << 2
    flags2 |= obj.unused_6 << 3
    flags2 |= obj.switched_off_original << 4
    flags2 |= obj.water_node << 5
    flags2 |= obj.highway_bridge << 6
    flags2 |= obj.switched_off << 7

    flags3 = 0
    flags3 |= obj.tunnel
    flags3 |= obj.heuretic * 2

    flags4 = 0
    flags4 |= obj.density & 0xF
    flags4 |= (obj.deadness & 0xF) << 4
    flags4 |= obj.left_turn_only << 7

    flags5 = 0
    flags5 |= obj.has_junction << 0
    flags5 |= speed_levels.index(obj.speed) << 1

    return flags0, flags1, flags2, flags3, flags4, flags5


def get_link_flags(obj):
    flags0 = 0
    flags0 |= obj.gps_both_ways << 0
    flags0 |= obj.block_if_no_lanes << 1
    flags0 |= obj.tilt << 2
    flags0 |= obj.tilt_falloff << 5

    flags1 = 0
    flags1 |= obj.tilt_falloff_2 << 0
    flags1 |= obj.narrow_road << 1
    flags1 |= obj.leads_to_dead_end << 2
    flags1 |= obj.leads_from_dead_end << 3
    flags1 |= obj.negative_offset << 7
    flags1 |= obj.width << 4

    flags2 = 0
    flags2 |= obj.dont_use_for_navigation << 0
    flags2 |= obj.shortcut << 1
    flags2 |= obj.bwd_lanes << 2
    flags2 |= obj.fwd_lanes << 5

    return flags0, flags1, flags2



def node_from_obj(obj):

    node = Node()
    node.area_id = obj.node_properties.area_id
    node.node_id = obj.node_properties.node_id
    node.streetname = obj.node_properties.streetname
    node.position = obj.location
    node.flags_0 = get_node_flags(obj.node_properties.flags)[0]
    node.flags_1 = get_node_flags(obj.node_properties.flags)[1]
    node.flags_2 = get_node_flags(obj.node_properties.flags)[2]
    node.flags_3 = get_node_flags(obj.node_properties.flags)[3]
    node.flags_4 = get_node_flags(obj.node_properties.flags)[4]
    node.flags_5 = get_node_flags(obj.node_properties.flags)[5]
    node.links = link_from_obj(obj.node_properties.links)
    return node


def link_from_obj(obj):
    links = []
    for link_obj in obj:
        link = Link()
        link.to_area_id = link_obj.to_area_id
        link.to_node_id = link_obj.to_node_id
        link.flags_0 = get_link_flags(link_obj.flags)[0]
        link.flags_1 = get_link_flags(link_obj.flags)[1]
        link.flags_2 = get_link_flags(link_obj.flags)[2]
        link.length = link_obj.length
        links.append(link)
    return links


def junction_from_obj(obj):

    junction = Junction()
    junction.position = mathutils.Vector((obj.position_x, obj.position_y))
    junction.min_z = obj.min_z
    junction.max_z = obj.max_z
    junction.size_x =  obj.size_x
    junction.size_y = obj.size_y
    junction.heightmap = obj.heightmap
    return junction


def junctionref_from_obj(obj):

    junctionref = JunctionRef()
    junctionref.area_id = obj.area_id
    junctionref.node_id = obj.node_id
    junctionref.junction_id = obj.junction_id
    junctionref.unk_0 = obj.unk_0
    return junctionref


def sorted_nodes_by_id(nodes):
    return sorted(nodes, key=lambda node: node.node_properties.node_id)

def ynd_from_object(obj):
    ynd = NodePath()

    ynd.vehicle_node_count = obj.node_path_properties.vehicle_node_count
    ynd.ped_node_count = obj.node_path_properties.ped_node_count

    for child in sorted_nodes_by_id(obj.children):
        ynd.nodes.append(node_from_obj(child))
        if child.node_properties.flags.has_junction:
            ynd.junctions.append(junction_from_obj(child.node_properties.junction))
            ynd.junctionrefs.append(junctionref_from_obj(child.node_properties.junctionref))
    return ynd


def export_ynd(obj: bpy.types.Object, filepath: str) -> bool:
    ynd = ynd_from_object(obj)
    ynd.write_xml(filepath)
    return True