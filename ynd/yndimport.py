import bpy
from ..cwxml.nodepath import YND
from ..sollumz_properties import SollumType
from ..tools.meshhelper import create_box
from .geonode import create_geonode, apply_geonode
from .utils import find_node
from ..tools.utils import get_filename

def set_node_flags0_values(obj, flags):
    obj.node_properties.flags.fill_group_1 = bool(flags & (1 << 0))
    obj.node_properties.flags.fill_group_2 = bool(flags & (1 << 1))
    obj.node_properties.flags.fill_group_3 = bool(flags & (1 << 2))
    obj.node_properties.flags.offroad = bool(flags & (1 << 3))
    obj.node_properties.flags.unused_4 = bool(flags & (1 << 4))
    obj.node_properties.flags.nobigvehicles = bool(flags & (1 << 5))
    obj.node_properties.flags.nogoright = bool(flags & (1 << 6))
    obj.node_properties.flags.nogoleft = bool(flags & (1 << 7))

def set_node_flags1_values(obj, flags):
    obj.node_properties.flags.slip_lane = bool(flags & (1 << 0))
    obj.node_properties.flags.indicate_keep_left = bool(flags & (1 << 1))
    obj.node_properties.flags.indicate_keep_right = bool(flags & (1 << 2))
    
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
        160: 'OFFROAD_JUNCTION'
    }
    
    special_type = special_types.get(flags, 'NONE')
    obj.node_properties.flags.special_type = special_type

def set_node_flags2_values(obj, flags):
    obj.node_properties.flags.no_gps = bool(flags & (1 << 0))
    obj.node_properties.flags.unused_5 = bool(flags & (1 << 1))
    obj.node_properties.flags.junction = bool(flags & (1 << 2))
    obj.node_properties.flags.unused_6 = bool(flags & (1 << 3))
    obj.node_properties.flags.switched_off_original = bool(flags & (1 << 4))
    obj.node_properties.flags.water_node = bool(flags & (1 << 5))
    obj.node_properties.flags.highway_bridge = bool(flags & (1 << 6))
    obj.node_properties.flags.switched_off = bool(flags & (1 << 7))

def set_node_flags3_values(obj, flags):
    obj.node_properties.flags.tunnel = bool(flags & 1)
    obj.node_properties.flags.heuretic = flags // 2

def set_node_flags4_values(obj, flags):
    obj.node_properties.flags.density = flags & 0xF
    obj.node_properties.flags.deadness = (flags >> 4) & 0xF
    obj.node_properties.flags.left_turn_only = bool(flags & 128)

def set_node_flags5_values(obj, flags):
    obj.node_properties.flags.has_heightmap = bool(flags & 1)

    speed_levels = ['SLOW', 'NORMAL', 'FAST', 'FASTER']
    index = min(flags // 2, len(speed_levels) - 1)
    obj.node_properties.flags.speed = speed_levels[index]


def set_link_flags0_values(obj, flags):
    obj.flags.gps_both_ways = bool(flags & (1 << 0))
    obj.flags.block_if_no_lanes = bool(flags & (1 << 1))
    obj.flags.tilt = flags // 4
    obj.flags.tilt_falloff = flags // 32


def set_link_flags1_values(obj, flags):
    obj.flags.tilt_falloff_2 = bool(flags & (1 << 0))
    obj.flags.narrow_road = bool(flags & (1 << 1))
    obj.flags.leads_to_dead_end = bool(flags & (1 << 2))
    obj.flags.leads_from_dead_end = bool(flags & (1 << 3))
    obj.flags.negative_offset = bool(flags & (1 << 7))
    obj.flags.width = flags // 16


def set_link_flags2_values(obj, flags):
    obj.flags.dont_use_for_navigation = bool(flags & (1 << 0))
    obj.flags.shortcut = bool(flags & (1 << 1))
    obj.flags.bwd_lanes = flags // 4
    obj.flags.fwd_lanes = flags // 32


def apply_node_properties(obj, node):
    obj.node_properties.area_id = node.area_id
    obj.node_properties.node_id = node.node_id
    obj.node_properties.streetname = node.streetname
    obj.location = node.position
    set_node_flags0_values(obj, node.flags_0)
    set_node_flags1_values(obj, node.flags_1)
    set_node_flags2_values(obj, node.flags_2)
    set_node_flags3_values(obj, node.flags_3)
    set_node_flags4_values(obj, node.flags_4)
    set_node_flags5_values(obj, node.flags_5)


    for i, link in enumerate(node.links):
        link_obj = obj.node_properties.links.add()
        apply_link_properties(link_obj, link)
        apply_geonode(obj, find_node(link_obj.to_area_id, link_obj.to_node_id), (i + 1))


def apply_link_properties(obj, link):
    obj.to_area_id = link.to_area_id
    obj.to_node_id = link.to_node_id
    set_link_flags0_values(obj, link.flags_0)
    set_link_flags1_values(obj, link.flags_1)
    set_link_flags2_values(obj, link.flags_2)
    obj.length = link.length
    obj.name = f"PathNode {link.to_area_id}.{link.to_node_id}"

    linked_node = find_node(link.to_area_id, link.to_node_id)
    if linked_node is not None:
        streetname = linked_node.node_properties.streetname
        obj.name = f"{obj.name} {f'({streetname})' if streetname else ''}"


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
    node_obj.lock_rotation = (True, True, True)
    node_obj.lock_scale = (True, True, True)
    
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
            apply_junctionref_properties(node_obj.node_properties.junctionref, junctionref)
            apply_junction_properties(node_obj.node_properties.junction, junction)


def ynd_to_obj(ynd, path):
    ynd_obj = bpy.data.objects.new(get_filename(path), None)
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
    return ynd_to_obj(ynd_xml, filepath)