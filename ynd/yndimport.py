import bpy
from mathutils import Vector
from ..sollumz_properties import SollumType
from .properties import (
    NodeDictionaryProperties, NodeProperties, LinkProperties, 
    SpecialTypes, SpecialTypesEnumItems, SpeedEnumItems, 
    NodeFlags0, NodeFlags1, NodeFlags2, NodeFlags3, NodeFlags4, NodeFlags5,
    LinkFlags0, LinkFlags1, LinkFlags2
    )
from ..cwxml.ynd import NodeDictionary, Node, Link, YND
from .. import logger
from ..tools.blenderhelper import create_empty_object
from ..tools.utils import int_to_bool_list
from .utils import find_node_obj


def int_to_special_type(num):
    return {int(item[2]): item[0] for item in SpecialTypesEnumItems}.get(num >> 3, SpecialTypes.NONE)

def int_to_speed(num):
    return [item[0] for item in SpeedEnumItems][num >> 1]

def int_to_xy(num):
    return num & 0x1F, num >> 5

def int_to_value(value: int, start_bit: int, num_bits: int) -> int:
    return (value >> start_bit) & (1 << num_bits) - 1


def apply_node_flags(node_props: NodeProperties, node: Node):
    flags0: NodeFlags0 = node_props.flags0
    [
        flags0.scripted,
        flags0.gps_enabled,
        flags0.unused_4,
        flags0.offroad,
        flags0.unused_16,
        flags0.no_big_vehicles,
        flags0.cannot_go_right,
        flags0.cannot_go_left
    ] = int_to_bool_list(node.flags_0, 8)

    flags1: NodeFlags1 = node_props.flags1
    [
        flags1.slip_lane,
        flags1.indicate_keep_left,
        flags1.indicate_keep_right,
    ] = int_to_bool_list(node.flags_1, 3)
    flags1.special_type = int_to_special_type(node.flags_1)

    flags2: NodeFlags2 = node_props.flags2
    [
        flags2.no_gps,
        flags2.unused_2,
        flags2.junction,
        flags2.unused_8,
        flags2.disabled_1,
        flags2.water_boats,
        flags2.Freeway,
        flags2.disabled_2
    ] = int_to_bool_list(node.flags_2, 8)

    flags3: NodeFlags3 = node_props.flags3
    [
        flags3.tunnel
    ] = int_to_bool_list(node.flags_3, 1)
    flags3.heuristic = int_to_value(node.flags_3, 1, 31)

    flags4: NodeFlags4 = node_props.flags4
    flags4.density = int_to_value(node.flags_4, 0, 4)
    flags4.deadendness = int_to_value(node.flags_4, 4, 3)
    flags4.left_turn_only = int_to_bool_list(node.flags_2, 8)[7]

    flags5: NodeFlags5 = node_props.flags5
    [
        flags5.left_turn_only
    ] = int_to_bool_list(node.flags_5, 1)
    flags5.speed = int_to_speed(node.flags_5)


def apply_link_flags(link_props: LinkProperties, link: Link):
        flags0: LinkFlags0 = link_props.flags0
        [
            flags0.gps_both_ways,
            flags0.block_if_no_lanes,
        ] = int_to_bool_list(link.flags_0, 2)
        flags0.unknown_1 = int_to_value(link.flags_0, 2, 3)
        flags0.unknown_2 = int_to_value(link.flags_0, 4, 3)

        flags1: LinkFlags1 = link_props.flags1
        [
            flags1.unused_1,
            flags1.narrow_road,
            flags1.dead_end,
            flags1.dead_end_exit,
        ] = int_to_bool_list(link.flags_1, 4)
        flags1.negative_offset = int_to_bool_list(link.flags_1, 8)[7]
        flags1.offset = int_to_value(link.flags_1, 4, 3)

        flags2: LinkFlags2 = link_props.flags2
        [
            flags2.dont_use_for_navigation,
            flags2.shortcut
        ] = int_to_bool_list(link.flags_2, 2)
        flags2.back_lanes = int_to_value(link.flags_2, 4, 3)
        flags2.forward_lanes = int_to_value(link.flags_2, 4, 3)


def node_to_obj(obj: bpy.types.Object, node: Node):
    node_obj = create_empty_object(SollumType.NODE, f"{node.area_id}, {node.node_id}, {node.streetname}")
    node_obj.empty_display_type = 'CUBE'
    node_obj.empty_display_size = 0.5
    node_obj.parent = obj
    node_obj.location = node.position
    node_obj.lock_rotation = (True, True, True)
    node_obj.lock_scale = (True, True, True)

    node_props: NodeProperties = node_obj.node_properties
    node_props.area_id = node.area_id
    node_props.node_id = node.node_id
    node_props.streetname = node.streetname or "0"
    apply_node_flags(node_props, node)

    for link in node.links:
        link_obj = node_props.links.add()
        link_obj.to_area_id = link.to_area_id
        link_obj.to_node_id = link.to_node_id
        apply_link_flags(link_obj, link)


def ynd_to_obj(ynd: NodeDictionary):
    area_id = ynd.nodes[0].area_id
    ynd_obj = create_empty_object(SollumType.NODE_DICTIONARY, f"nodes{area_id}")
    ynd_obj.lock_location = (True, True, True)
    ynd_obj.lock_rotation = (True, True, True)
    ynd_obj.lock_scale = (True, True, True)

    ynd_props: NodeDictionaryProperties = ynd_obj.node_dictionary_properties
    ynd_props.x, ynd_props.y = int_to_xy(area_id)
    
    for node in ynd.nodes:
        node_to_obj(ynd_obj, node)

    for node_obj in ynd_obj.children:
        for link in node_obj.node_properties.links:
            link.linked_obj = find_node_obj(link.to_area_id, link.to_node_id)
            if link.linked_obj:
                linked_obj_props = link.linked_obj.node_properties
                link.name = f"{linked_obj_props.area_id}, {linked_obj_props.node_id}, {linked_obj_props.streetname}"
            else:
                link.name = f"{link.to_area_id}, {link.to_node_id}, ???"

def import_ynd(filepath):
    ynd_xml: NodeDictionary = YND.from_xml_file(filepath)
    found = False
    for obj in bpy.context.scene.objects:
        if obj.sollum_type == SollumType.NODE_DICTIONARY and obj.name == ynd_xml.name:
            logger.error(
                f"{ynd_xml.name} is already existing in the scene. Aborting.")
            found = True
            break
    if not found:
        obj = ynd_to_obj(ynd_xml)
