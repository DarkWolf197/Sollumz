import bpy
from bpy.props import (FloatProperty, CollectionProperty, PointerProperty,
                       StringProperty, IntProperty, FloatVectorProperty)


class JunctionRefProperties(bpy.types.PropertyGroup):
    area_id: IntProperty("AreaID")
    node_id: IntProperty("NodeID")
    junction_id: IntProperty("JunctionID")
    unk_0: IntProperty("Unk0")


class JunctionProperties(bpy.types.PropertyGroup):
    position: FloatVectorProperty(name="Position", default=(0, 0, 0), size=3, subtype='XYZ')
    min_z: FloatProperty(name="Min Z")
    max_z: FloatProperty(name="Max Z")
    size_x: IntProperty(name="Size X")
    size_y: IntProperty(name="Size Y")
    heightmap: StringProperty(name="Heightmap", default="")


class LinkProperties(bpy.types.PropertyGroup):
    to_area_id: IntProperty(name="To Area ID")
    to_node_id: IntProperty(name="To Node ID")
    flags_0: IntProperty(name="Flags 0")
    flags_1: IntProperty(name="Flags 1")
    flags_2: IntProperty(name="Flags 2")
    length: IntProperty(name="Link Lenght")


class NodeProperties(bpy.types.PropertyGroup):
    area_id: IntProperty(name="Area ID")
    node_id: IntProperty(name="Node ID")
    streetname: StringProperty(name="Street Name", default="")
    position: FloatVectorProperty(name="Position", default=(0, 0, 0), size=3, subtype='XYZ')
    flags_0: IntProperty(name="Flags 0")
    flags_1: IntProperty(name="Flags 1")
    flags_2: IntProperty(name="Flags 2")
    flags_3: IntProperty(name="Flags 3")
    flags_4: IntProperty(name="Flags 4")
    flags_5: IntProperty(name="Flags 5")
    links: CollectionProperty(type=LinkProperties)


class NodePathProperties(bpy.types.PropertyGroup):
    vehicle_node_count: IntProperty("VehicleNodeCount")
    ped_node_count: IntProperty("PedNodeCount")
    nodes: CollectionProperty(type=NodeProperties)
    junctions: CollectionProperty(type=JunctionProperties)
    junctionrefs: CollectionProperty(type=JunctionRefProperties)


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