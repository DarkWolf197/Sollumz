import bpy
from bpy.props import (FloatProperty, CollectionProperty, PointerProperty, BoolProperty,
                       StringProperty, IntProperty, FloatVectorProperty, EnumProperty)
from ..tools.utils import int_to_bool_list, flag_prop_to_list, flag_list_to_int


class NodeFlags_0_PropertyGroup(bpy.types.PropertyGroup):
    def update_flags_total(self, context):
        flags = int_to_bool_list(int(self.flags_0), size=8)
        for index, flag_name in enumerate(NodeFlags_0.__annotations__):
            self.flags_0_toggle[flag_name] = flags[index]

    def update_flag(self, context):
        flags = flag_prop_to_list(self.__class__.__annotations__, self)
        obj = context.active_object
        if obj:
            obj.node_properties.flags_0 = flag_list_to_int(flags)

class NodeFlags_0(bpy.types.PropertyGroup):
    scripted: BoolProperty(
        name="Scripted", update=NodeFlags_0_PropertyGroup.update_flag)
    gps_enabled: BoolProperty(
        name="GPS Enabled", update=NodeFlags_0_PropertyGroup.update_flag)
    unused_4: BoolProperty(
        name="Unused 4", update=NodeFlags_0_PropertyGroup.update_flag)
    offroad: BoolProperty(
        name="Offroad", update=NodeFlags_0_PropertyGroup.update_flag)
    unused_16: BoolProperty(
        name="Unused 16", update=NodeFlags_0_PropertyGroup.update_flag)
    nobigvehicles: BoolProperty(
        name="No Big Vehicles", update=NodeFlags_0_PropertyGroup.update_flag)
    nogoright: BoolProperty(
        name="Cannot Go Right", update=NodeFlags_0_PropertyGroup.update_flag)
    nogoleft: BoolProperty(
        name="Cannot Go Left", update=NodeFlags_0_PropertyGroup.update_flag)



class NodeFlags_1_PropertyGroup(bpy.types.PropertyGroup):
    def update_flags_total(self, context):
        flags = int_to_bool_list(int(self.flags_1), size=8)
        for index, flag_name in enumerate(NodeFlags_1.__annotations__):
            self.flags_1_toggle[flag_name] = flags[index]

    def update_flag(self, context):
        flags = flag_prop_to_list(self.__class__.__annotations__, self)
        obj = context.active_object
        if obj:
            obj.node_properties.flags_1 = flag_list_to_int(flags)

class NodeFlags_1(bpy.types.PropertyGroup):
    slip_lane: BoolProperty(
        name="Slip Lane", update=NodeFlags_1_PropertyGroup.update_flag)
    indicate_keep_left: BoolProperty(
        name="Indicate Keep Left", update=NodeFlags_1_PropertyGroup.update_flag)
    indicate_keep_right: BoolProperty(
        name="Indicate Keep Right", update=NodeFlags_1_PropertyGroup.update_flag)
    special_type: EnumProperty(
        name="Special Type",
        items=[
            ('NONE', "None", "None"),
            ('PARKING', "Parking Space", "Parking Space"),
            ('PED_CROSSING', "PedNodeRoadCrossing", "PedNodeRoadCrossing"),
            ('PED_ASSISTED', "PedNodeAssistedMovement", "PedNodeAssistedMovement"),
            ('TRAFFIC_LIGHT', "TrafficLightJunctionStop", "TrafficLightJunctionStop"),
            ('STOP_SIGN', "Stop Sign", "Stop Sign"),
            ('CAUTION', "Caution", "Caution"),
            ('PED_CROSSING_NOWAIT', "PedRoadCrossingNoWait", "PedRoadCrossingNoWait"),
            ('EMERGENCY_VEHICLES', "EmergencyVehiclesOnly", "EmergencyVehiclesOnly"),
            ('OFFROAD_JUNCTION', "OffRoadJunction", "OffRoadJunction")
        ],
        update=NodeFlags_1_PropertyGroup.update_flag
    )



class NodeFlags_2_PropertyGroup(bpy.types.PropertyGroup):
    def update_flags_total(self, context):
        flags = int_to_bool_list(int(self.flags_2), size=8)
        for index, flag_name in enumerate(NodeFlags_2.__annotations__):
            self.flags_2_toggle[flag_name] = flags[index]

    def update_flag(self, context):
        flags = flag_prop_to_list(self.__class__.__annotations__, self)
        obj = context.active_object
        if obj:
            obj.node_properties.flags_2 = flag_list_to_int(flags)

class NodeFlags_2(bpy.types.PropertyGroup):
    no_gps: BoolProperty(
        name="No GPS", update=NodeFlags_2_PropertyGroup.update_flag)
    unused_2: BoolProperty(
        name="Unused 2", update=NodeFlags_2_PropertyGroup.update_flag)
    junction: BoolProperty(
        name="Junction", update=NodeFlags_2_PropertyGroup.update_flag)
    unused_8: BoolProperty(
        name="Unused 8", update=NodeFlags_2_PropertyGroup.update_flag)
    disabled_1: BoolProperty(
        name="Disabled/Unk 2", update=NodeFlags_2_PropertyGroup.update_flag)
    water_boats: BoolProperty(
        name="Water/Boats", update=NodeFlags_2_PropertyGroup.update_flag)
    freeway: BoolProperty(
        name="Freeway", update=NodeFlags_2_PropertyGroup.update_flag)
    disabled_2: BoolProperty(
        name="Disabled/Unk 2", update=NodeFlags_2_PropertyGroup.update_flag)


class JunctionProperties(bpy.types.PropertyGroup):
    position: FloatVectorProperty(name="Position", default=(0, 0, 0), size=3, subtype='XYZ')
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
    flags_0: IntProperty(name="Flags 0")
    flags_1: IntProperty(name="Flags 1")
    flags_2: IntProperty(name="Flags 2")
    length: IntProperty(name="Link Lenght")


class NodeProperties(bpy.types.PropertyGroup):
    area_id: IntProperty(name="Area ID")
    node_id: IntProperty(name="Node ID")
    streetname: StringProperty(name="Street Name", default="")
    position: FloatVectorProperty(name="Position", default=(0, 0, 0), size=3, subtype='XYZ')
    flags_0: IntProperty(name="Flags 0", default=0, min=0, max=255,
                       update=NodeFlags_0_PropertyGroup.update_flags_total)
    flags_1: IntProperty(name="Flags 1")
    flags_2: IntProperty(name="Flags 2")
    flags_3: IntProperty(name="Flags 3")
    flags_4: IntProperty(name="Flags 4")
    flags_5: IntProperty(name="Flags 5")
    links: CollectionProperty(type=LinkProperties)
    junction_found: BoolProperty(name="Junction Found", default=False)
    junctionref: PointerProperty(type=JunctionRefProperties)
    junction: PointerProperty(type=JunctionProperties)

    flags_0_toggle: PointerProperty(type=NodeFlags_0)
    node_flags_0_toggle: PointerProperty(type=NodeFlags_0_PropertyGroup)

    flags_1_toggle: PointerProperty(type=NodeFlags_1)
    node_flags_1_toggle: PointerProperty(type=NodeFlags_1_PropertyGroup)

    flags_2_toggle: PointerProperty(type=NodeFlags_2)
    node_flags_2_toggle: PointerProperty(type=NodeFlags_2_PropertyGroup)

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