import bpy
from bpy.props import (FloatProperty, CollectionProperty, PointerProperty, BoolProperty,
                       StringProperty, IntProperty, FloatVectorProperty)
from .flags import NodeFlags, LinkFlags

class JunctionProperties(bpy.types.PropertyGroup):
    position_x: FloatProperty(name="Pos X")
    position_y: FloatProperty(name="Pos Y")
    min_z: FloatProperty(name="Min Z")
    max_z: FloatProperty(name="Max Z")
    size_x: IntProperty(name="Size X")
    size_y: IntProperty(name="Size Y")
    heightmap: StringProperty(name="Heightmap", default="")


class JunctionRefProperties(bpy.types.PropertyGroup):
    area_id: IntProperty("AreaID")
    node_id: IntProperty("NodeID")
    junction_id: IntProperty("JunctionID")
    unk_0: IntProperty("Unk0")


class LinkProperties(bpy.types.PropertyGroup):
    to_area_id: IntProperty(name="To Area ID")
    to_node_id: IntProperty(name="To Node ID")
    flags: PointerProperty(type=LinkFlags, name="Flags")
    length: IntProperty(name="Link Lenght")

    name: StringProperty(name="")
    linked_obj: PointerProperty(type=bpy.types.Object, name="Linked")


class NodeProperties(bpy.types.PropertyGroup):
    area_id: IntProperty(name="Area ID")
    node_id: IntProperty(name="Node ID")
    streetname: StringProperty(name="Street Name", default="")
    position: FloatVectorProperty(name="Position", default=(0, 0, 0), size=3, subtype='XYZ')
    flags: PointerProperty(type=NodeFlags, name="Flags")
    links: CollectionProperty(type=LinkProperties)
    link_index: IntProperty(name="Link Index")
    junctionref: PointerProperty(type=JunctionRefProperties)
    junction: PointerProperty(type=JunctionProperties)


class NodePathProperties(bpy.types.PropertyGroup):
    vehicle_node_count: IntProperty("VehicleNodeCount")
    ped_node_count: IntProperty("PedNodeCount")
    nodes: CollectionProperty(type=NodeProperties)
    junctions: CollectionProperty(type=JunctionProperties)


def register():
    bpy.types.Object.node_path_properties = PointerProperty(type=NodePathProperties)
    bpy.types.Object.node_properties = PointerProperty(type=NodeProperties)
    bpy.types.Object.link_properties = PointerProperty(type=LinkProperties)
    bpy.types.Object.junction_properties = PointerProperty(type=JunctionProperties)
    bpy.types.Object.junctionref_properties = PointerProperty(type=JunctionRefProperties)


def unregister():
    del bpy.types.Object.node_path_properties
    del bpy.types.Object.node_properties
    del bpy.types.Object.link_properties
    del bpy.types.Object.junction_properties
    del bpy.types.Object.junctionref_properties