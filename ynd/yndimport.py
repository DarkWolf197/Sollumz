import bpy
from ..cwxml.nodepath import YND
from ..sollumz_properties import SollumType
from ..tools.meshhelper import create_box
from .geonode import create_geonode, apply_geonode
from .utils import find_node
from ..tools.utils import get_filename


special_types = {
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

def set_node_flags(obj, flags0, flags1, flags2, flags3, flags4, flags5):
    obj.fill_group_1 =              bool(flags0 & (1 << 0))
    obj.fill_group_2 =              bool(flags0 & (1 << 1))
    obj.fill_group_3 =              bool(flags0 & (1 << 2))
    obj.offroad =                   bool(flags0 & (1 << 3))
    obj.unused_4 =                  bool(flags0 & (1 << 4))
    obj.nobigvehicles =             bool(flags0 & (1 << 5))
    obj.nogoright =                 bool(flags0 & (1 << 6))
    obj.nogoleft =                  bool(flags0 & (1 << 7))

    obj.slip_lane =                 bool(flags1 & (1 << 0))
    obj.indicate_keep_left =        bool(flags1 & (1 << 1))
    obj.indicate_keep_right =       bool(flags1 & (1 << 2))
    obj.special_type =              special_types.get(flags1 & ~((1 << 0) | (1 << 1) | (1 << 2)), 'NONE')

    obj.no_gps =                    bool(flags2 & (1 << 0))
    obj.unused_5 =                  bool(flags2 & (1 << 1))
    obj.junction =                  bool(flags2 & (1 << 2))
    obj.unused_6 =                  bool(flags2 & (1 << 3))
    obj.switched_off_original =     bool(flags2 & (1 << 4))
    obj.water_node =                bool(flags2 & (1 << 5))
    obj.highway_bridge =            bool(flags2 & (1 << 6))
    obj.switched_off =              bool(flags2 & (1 << 7))

    obj.tunnel =                    bool(flags3 & (1 << 0))
    obj.heuretic =                  int((flags3 >> 1) & 127)

    obj.density =                   int((flags4) & 15)
    obj.deadness =                  int((flags4 >> 4) & 7)
    obj.left_turn_only =            bool(flags4 & (1 << 7))

    obj.has_junction =              bool(flags5 & (1 << 0))
    obj.speed =                     speed_levels[flags5 >> 1]


def set_link_flags(obj, flags0, flags1, flags2):
    obj.gps_both_ways =             bool(flags0 & (1 << 0))
    obj.block_if_no_lanes =         bool(flags0 & (1 << 1))
    obj.tilt =                      int((flags0 >> 2) & 7)
    obj.tilt_falloff =              int((flags0 >> 5) & 7)

    obj.tilt_falloff_2 =            bool(flags1 & (1 << 0))
    obj.narrow_road =               bool(flags1 & (1 << 1))
    obj.leads_to_dead_end =         bool(flags1 & (1 << 2))
    obj.leads_from_dead_end =       bool(flags1 & (1 << 3))
    obj.negative_offset =           bool(flags1 & (1 << 7))
    obj.offset =                    int(flags1 >> 4 & 7)

    obj.dont_use_for_navigation =   bool(flags2 & (1 << 0))
    obj.shortcut =                  bool(flags2 & (1 << 1))
    obj.bwd_lanes =                 int((flags2 >> 2) & 7)
    obj.fwd_lanes =                 int((flags2 >> 5) & 7)



def apply_node_properties(obj, node):
    obj.node_properties.area_id = node.area_id
    obj.node_properties.node_id = node.node_id
    obj.node_properties.streetname = node.streetname
    obj.location = node.position
    set_node_flags(obj.node_properties.flags, node.flags_0, node.flags_1, node.flags_2, node.flags_3, node.flags_4, node.flags_5)
    for i, link in enumerate(node.links):
        link_obj = obj.node_properties.links.add()
        apply_link_properties(link_obj, link)
        apply_geonode(obj, find_node(link_obj.to_area_id, link_obj.to_node_id), (i + 1))


def apply_link_properties(obj, link):
    obj.to_area_id = link.to_area_id
    obj.to_node_id = link.to_node_id
    set_link_flags(obj.flags, link.flags_0, link.flags_1, link.flags_2)
    obj.length = link.length
    obj.name = f"PathNode {link.to_area_id}.{link.to_node_id}"
    linked_node = find_node(link.to_area_id, link.to_node_id)
    if linked_node is not None:
        streetname = linked_node.node_properties.streetname
        obj.name = f"{obj.name} {f'({streetname})' if streetname else ''}"
        obj.linked_obj = linked_node


def apply_junctionref_properties(obj, junctionref):
    obj.area_id = junctionref.area_id
    obj.node_id = junctionref.node_id
    obj.junction_id = junctionref.junction_id
    obj.unk_0 = junctionref.unk_0


def apply_junction_properties(obj, junction):
    obj.position_x = junction.position[0]
    obj.position_y = junction.position[1]
    obj.min_z = junction.min_z
    obj.max_z = junction.max_z
    obj.size_x = junction.size_x
    obj.size_y = junction.size_y
    obj.heightmap = junction.heightmap


def node_to_obj(parent_obj: bpy.types.Object, node):
    mesh_name = "Node Mesh"
    if mesh_name in bpy.data.meshes:
        mesh = bpy.data.meshes[mesh_name]
    else:
        mesh = bpy.data.meshes.new(mesh_name)
        create_box(mesh, size=0.5)

    node_obj = bpy.data.objects.new("PathNode", mesh)
    node_obj.sollum_type = SollumType.TRAFFIC_NODE
    node_obj.lock_rotation = (True, True, True)
    node_obj.lock_scale = (True, True, True)

    node_obj.parent = parent_obj

    bpy.context.collection.objects.link(node_obj)
    bpy.context.view_layer.objects.active = node_obj

    apply_node_properties(node_obj, node)
    node_obj.name = f"PathNode {node.area_id}.{node.node_id}"

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