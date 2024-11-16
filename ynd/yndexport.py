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
    if obj.fill_group_1:                flags0 |= (1 << 0)
    if obj.fill_group_2:                flags0 |= (1 << 1)
    if obj.fill_group_3:                flags0 |= (1 << 2)
    if obj.offroad:                     flags0 |= (1 << 3)
    if obj.unused_4:                    flags0 |= (1 << 4)
    if obj.nobigvehicles:               flags0 |= (1 << 5)
    if obj.nogoright:                   flags0 |= (1 << 6)
    if obj.nogoleft:                    flags0 |= (1 << 7)

    flags1 = 0  
    if obj.slip_lane:                   flags1 |= (1 << 0)
    if obj.indicate_keep_left:          flags1 |= (1 << 1)
    if obj.indicate_keep_right:         flags1 |= (1 << 2)
    
    for flag_value, type_name in special_types.items():
        if type_name == obj.special_type:
            flags1 |= flag_value
            break
    
    flags2 = 0
    if obj.no_gps:                      flags2 |= (1 << 0)
    if obj.unused_5:                    flags2 |= (1 << 1)
    if obj.junction:                    flags2 |= (1 << 2)
    if obj.unused_6:                    flags2 |= (1 << 3)
    if obj.switched_off_original:       flags2 |= (1 << 4)
    if obj.water_node:                  flags2 |= (1 << 5)
    if obj.highway_bridge:              flags2 |= (1 << 6)
    if obj.switched_off:                flags2 |= (1 << 7)

    flags3 = 0
    if obj.tunnel:                      flags3 |= (1 << 0)
    flags3 |= (obj.heuretic & 127) << 1

    flags4 = 0
    flags4 |= obj.density & 15
    flags4 |= (obj.deadness & 7) << 4
    if obj.left_turn_only:              flags4 |= (1 << 7)

    flags5 = 0
    if obj.has_junction:                flags5 |= (1 << 0)
    for speed_index, speed_value in enumerate(speed_levels):
        if speed_value == obj.speed:
            flags5 |= speed_index << 1
            break

    return flags0, flags1, flags2, flags3, flags4, flags5


def get_link_flags(obj):

    flags0 = 0
    if obj.gps_both_ways:           flags0 |= (1 << 0)
    if obj.block_if_no_lanes:       flags0 |= (1 << 1)
    flags0 |=                       (obj.tilt & 7) << 2
    flags0 |=                       (obj.tilt_falloff & 7) << 5

    flags1 = 0
    if obj.tilt_falloff_2:          flags1 |= (1 << 0)
    if obj.narrow_road:             flags1 |= (1 << 1)
    if obj.leads_to_dead_end:       flags1 |= (1 << 2)
    if obj.leads_from_dead_end:     flags1 |= (1 << 3)
    if obj.negative_offset:         flags1 |= (1 << 7)
    flags1 |=                       (obj.offset & 7) << 4

    flags2 = 0
    if obj.dont_use_for_navigation: flags2 |= (1 << 0)
    if obj.shortcut:                flags2 |= (1 << 1)
    flags2 |=                       (obj.bwd_lanes & 7) << 2
    flags2 |=                       (obj.fwd_lanes & 7) << 5

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