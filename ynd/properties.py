import bpy
from bpy.props import (FloatProperty, CollectionProperty, PointerProperty, BoolProperty,
                       StringProperty, IntProperty, FloatVectorProperty, EnumProperty)
from enum import Enum
from mathutils import Vector
from ..tools.utils import get_list_item


def xy_to_flag(x: int, y: int) -> int:
    return (y << 5) | x

class Speed(str, Enum):
    SLOW = "sollumz_slow"
    NORMAL = "sollumz_normal"
    FAST = "sollumz_fast"
    FASTER = "sollumz_faster"

SpeedEnumItems = (
    (Speed.SLOW, "Slow", "", 0),
    (Speed.NORMAL, "Normal", "", 1),
    (Speed.FAST, "Fast", "", 2),
    (Speed.FASTER, "Faster", "", 3)
)

class SpecialTypes(str, Enum):
    NONE = "sollumz_none"
    PARKING_SPACE = "sollumz_parking_space"
    PED_NODE_ROAD_CROSSING = "sollumz_ped_node_road_crossing"
    PED_NODE_ASSISTED_MOVEMENT = "sollumz_ped_node_assisted_movement"
    TRAFFIC_LIGHT_JUNCTION_STOP = "sollumz_traffic_light_junction_stop"
    STOP_SIGN = "sollumz_stop_sign"
    CAUTION = "sollumz_caution"
    PED_ROAD_CROSSING_NO_WAIT = "sollumz_ped_road_crossing_no_wait"
    EMERGENCY_VEHICLES_ONLY = "sollumz_emergency_vehicles_only"
    OFF_ROAD_JUNCTION = "sollumz_off_road_junction"

SpecialTypesEnumItems = (
    (SpecialTypes.NONE, "None", "0", 0),
    (SpecialTypes.PARKING_SPACE, "Parking Space", "2", 1),
    (SpecialTypes.PED_NODE_ROAD_CROSSING, "PedNode Road Crossing", "10", 2),
    (SpecialTypes.PED_NODE_ASSISTED_MOVEMENT, "PedNode Assisted Movement", "14", 3),
    (SpecialTypes.TRAFFIC_LIGHT_JUNCTION_STOP, "Traffic Light Junction Stop", "15", 4),
    (SpecialTypes.STOP_SIGN, "Stop Sign", "16", 5),
    (SpecialTypes.CAUTION, "Caution", "17", 6),
    (SpecialTypes.PED_ROAD_CROSSING_NO_WAIT, "PedRoad Crossing NoWait", "18", 7),
    (SpecialTypes.EMERGENCY_VEHICLES_ONLY, "Emergency Vehicles Only", "19", 8),
    (SpecialTypes.OFF_ROAD_JUNCTION, "Offroad Junction", "20", 9)
)

PedNodes = (
    SpecialTypes.PED_NODE_ROAD_CROSSING,
    SpecialTypes.PED_NODE_ASSISTED_MOVEMENT,
    SpecialTypes.PED_ROAD_CROSSING_NO_WAIT
)


class NodeFlags0(bpy.types.PropertyGroup):
    scripted: BoolProperty(name="Scripted")
    gps_enabled: BoolProperty(name="GPS Enabled")
    unused_4: BoolProperty(name="Unused 4")
    offroad: BoolProperty(name="Offroad")
    unused_16: BoolProperty(name="Unused 16")
    no_big_vehicles: BoolProperty(name="No Big Vehicles")
    cannot_go_right: BoolProperty(name="Cannot Go Right")
    cannot_go_left: BoolProperty(name="Cannot Go Left")

class NodeFlags1(bpy.types.PropertyGroup):
    slip_lane: BoolProperty(name="Slip Lane")
    indicate_keep_left: BoolProperty(name="Indicate Keep Left")
    indicate_keep_right: BoolProperty(name="Indicate Keep Right")
    special_type: EnumProperty(items=SpecialTypesEnumItems, name="Special Type")

class NodeFlags2(bpy.types.PropertyGroup):
    no_gps: BoolProperty(name="No GPS")
    unused_2: BoolProperty(name="Unused 2")
    junction: BoolProperty(name="Junction")
    unused_8: BoolProperty(name="Unused 8")
    disabled_1: BoolProperty(name="Disabled 1")
    water_boats: BoolProperty(name="Water/Boats")
    Freeway: BoolProperty(name="Freeway")
    disabled_2: BoolProperty(name="Disabled 2")

class NodeFlags3(bpy.types.PropertyGroup):
    tunnel: BoolProperty(name="Tunnel")
    heuristic: IntProperty(name="Heuristic", min=0, max=127)

class NodeFlags4(bpy.types.PropertyGroup):
    density: IntProperty(name="Density", min=0, max=15)
    deadendness: IntProperty(name="Deadendness", min=0, max=7)
    left_turn_only: BoolProperty(name="Left Turn Only")

class NodeFlags5(bpy.types.PropertyGroup):
    has_junction_heightmap: BoolProperty(name="Has Junction Heightmap")
    speed: EnumProperty(items=SpeedEnumItems, name="Speed")


class LinkFlags0(bpy.types.PropertyGroup):
    gps_both_ways: BoolProperty(name="GPS Both Ways")
    block_if_no_lanes: BoolProperty(name="Block if no lanes")
    unknown_1: IntProperty(name="Unknown 1", min=0, max=7)
    unknown_2: IntProperty(name="Unknown 2", min=0, max=7)

class LinkFlags1(bpy.types.PropertyGroup):
    unused_1: BoolProperty(name="Unused_1")
    narrow_road: BoolProperty(name="Narrow_Road")
    dead_end: BoolProperty(name="Dead_End")
    dead_end_exit: BoolProperty(name="Dead_End_Exit")
    negative_offset: BoolProperty(name="Negative_Offset")
    offset: IntProperty(name="Offset", min=0, max=7)

class LinkFlags2(bpy.types.PropertyGroup):
    dont_use_for_navigation: BoolProperty(name="Don't Use For Navigation")
    shortcut: BoolProperty(name="Shortcut")
    back_lanes: IntProperty(name="Back Lanes", min=0, max=7)
    forward_lanes: IntProperty(name="Forward Lanes", min=0, max=7)


class JunctionProperties(bpy.types.PropertyGroup):
    max_z: FloatProperty(name="Max Z")
    min_z: FloatProperty(name="Min Z")
    pos_x: FloatProperty(name="Pos X")
    pos_y: FloatProperty(name="Pos Y")
    size_x: IntProperty(name="Size X")
    size_y: IntProperty(name="Size Y")
    heightmap: StringProperty(name="Heightmap")


class JunctionRefProperties(bpy.types.PropertyGroup):
    area_id: IntProperty("Area ID")
    node_id: IntProperty("Node ID")
    junction_id: IntProperty("JunctionID")
    unk_0: IntProperty("Unk0")


class LinkProperties(bpy.types.PropertyGroup):
    to_area_id: IntProperty(name="To Area ID")
    to_node_id: IntProperty(name="To Node ID")
    flags0: PointerProperty(type=LinkFlags0, name="Flags 0")
    flags1: PointerProperty(type=LinkFlags1, name="Flags 1")
    flags2: PointerProperty(type=LinkFlags2, name="Flags 2")
    length: IntProperty(name="Link Lenght")
    linked_obj: PointerProperty(type=bpy.types.Object, name="Linked")

    @property
    def length(self):
        obj = self.id_data
        distance = (obj.location - self.linked_obj.location).length
        return int(min(255, distance))
    


class NodeProperties(bpy.types.PropertyGroup):
    def update_node_name(self, context):
        obj = self.id_data
        obj.name = f"{self.area_id}, {self.node_id}, {self.streetname}"

    area_id: IntProperty(
        name="Area ID", update=update_node_name, min=0)
    node_id: IntProperty(
        name="Node ID", update=update_node_name, min=0)
    streetname: StringProperty(
        name="Street Name", update=update_node_name)
    position: FloatVectorProperty(name="Position", subtype='XYZ')
    flags0: PointerProperty(type=NodeFlags0, name="Flags 0")
    flags1: PointerProperty(type=NodeFlags1, name="Flags 1")
    flags2: PointerProperty(type=NodeFlags2, name="Flags 2")
    flags3: PointerProperty(type=NodeFlags3, name="Flags 3")
    flags4: PointerProperty(type=NodeFlags4, name="Flags 4")
    flags5: PointerProperty(type=NodeFlags5, name="Flags 5")
    links: CollectionProperty(type=LinkProperties, name="Links")
    link_index: IntProperty(name="Link")
    junction: PointerProperty(type=JunctionProperties)


class NodeDictionaryProperties(bpy.types.PropertyGroup):
    prev_x: IntProperty(default=0)
    prev_y: IntProperty(default=0)

    def update_ynd(self, context):
        obj = self.id_data
        flag = xy_to_flag(self.x, self.y)

        obj.name = f"nodes{str(flag)}"
        
        offset = Vector(((self.x - self.prev_x) * 512, (self.y - self.prev_y) * 512, 0))
        for child in obj.children:
            node_props = child.node_properties
            child.location += offset
            node_props.area_id = flag
        
        self.prev_x, self.prev_y = self.x, self.y

    x: IntProperty(name="X", min=0, max=31, update=update_ynd)
    y: IntProperty(name="Y", min=0, max=31, update=update_ynd)

    @property
    def ped_node_count(self):
        obj = self.id_data
        return len([c for c in obj.children if c.node_properties.flags1.special_type in PedNodes])

    @property
    def vehicle_node_count(self):
        obj = self.id_data
        return len([c for c in obj.children if c.node_properties.flags1.special_type not in PedNodes])


def register():
    bpy.types.Object.node_dictionary_properties = PointerProperty(type=NodeDictionaryProperties)
    bpy.types.Object.node_properties = PointerProperty(type=NodeProperties)

def unregister():
    del bpy.types.Object.node_dictionary_properties
    del bpy.types.Object.node_properties