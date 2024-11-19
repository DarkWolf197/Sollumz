import bpy
from pathlib import Path
from mathutils import Vector
from ..sollumz_properties import SOLLUMZ_UI_NAMES, SollumType
from ..tools.meshhelper import create_box


def create_nodedict(name="nodes", sollum_type=SollumType.NODE_DICTIONARY):
    empty = bpy.data.objects.new(SOLLUMZ_UI_NAMES[sollum_type], None)
    empty.empty_display_size = 0
    empty.sollum_type = sollum_type
    empty.name = name
    empty.lock_location = (True, True, True)
    empty.lock_rotation = (True, True, True)
    empty.lock_scale = (True, True, True)
    bpy.context.collection.objects.link(empty)
    return empty

def create_node(parent_obj=None, sollum_type=SollumType.TRAFFIC_NODE):
    mesh_name = "Node Mesh"
    if mesh_name in bpy.data.meshes:
        mesh = bpy.data.meshes[mesh_name]
    else:
        mesh = bpy.data.meshes.new(mesh_name)
        create_box(mesh, size=0.5)

    node_obj = bpy.data.objects.new(SOLLUMZ_UI_NAMES[sollum_type], mesh)
    node_obj.sollum_type = sollum_type
    node_obj.lock_rotation = (True, True, True)
    node_obj.lock_scale = (True, True, True)
    node_obj.parent = parent_obj

    bpy.context.collection.objects.link(node_obj)
    bpy.context.view_layer.objects.active = node_obj

    node_obj.name = f"PathNode UNSET.UNSET"

    return node_obj