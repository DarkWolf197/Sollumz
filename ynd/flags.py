import bpy
from ..sollumz_properties import FlagPropertyGroup

special_types = [('NONE', "None", ""),
                 ('PARKING', "Parking Space", ""),
                 ('PED_CROSSING', "PedNodeRoadCrossing", ""),
                 ('PED_ASSISTED', "PedNodeAssistedMovement", ""),
                 ('TRAFFIC_LIGHT', "TrafficLightJunctionStop", ""),
                 ('STOP_SIGN', "Stop Sign", ""),
                 ('CAUTION', "Caution", ""),
                 ('PED_CROSSING_NOWAIT', "PedRoadCrossingNoWait", ""),
                 ('EMERGENCY_VEHICLES', "EmergencyVehiclesOnly", ""),
                 ('OFFROAD_JUNCTION', "OffRoadJunction", "")]

speeds = [('SLOW', "Slow", ""),
          ('NORMAL', "Normal", ""),
          ('FAST', "Fast", ""),
          ('FASTER', "Faster", "")]


class NodeFlags(FlagPropertyGroup, bpy.types.PropertyGroup):
    size = 27

    # Flags0
    fill_group_1: bpy.props.BoolProperty(
        name="Fill Group 1")
    fill_group_2: bpy.props.BoolProperty(
        name="Fill Group 2")
    fill_group_3: bpy.props.BoolProperty(
        name="Fill Group 3")
    offroad: bpy.props.BoolProperty(
        name="Offroad")
    unused_4: bpy.props.BoolProperty(
        name="Unused 4")
    nobigvehicles: bpy.props.BoolProperty(
        name="No Big Vehicles")
    nogoright: bpy.props.BoolProperty(
        name="Cannot Go Right")
    nogoleft: bpy.props.BoolProperty(
        name="Cannot Go Left")

    # Flags1
    slip_lane: bpy.props.BoolProperty(
        name="Slip Lane")
    indicate_keep_left: bpy.props.BoolProperty(
        name="Indicate Keep Left")
    indicate_keep_right: bpy.props.BoolProperty(
        name="Indicate Keep Right")
    special_type: bpy.props.EnumProperty(
        items=special_types, name="Special Type")

    # Flags2
    no_gps: bpy.props.BoolProperty(
        name="No GPS")
    unused_5: bpy.props.BoolProperty(
        name="Unused 5")
    junction: bpy.props.BoolProperty(
        name="Junction")
    unused_6: bpy.props.BoolProperty(
        name="Unused 6")
    switched_off_original: bpy.props.BoolProperty(
        name="Switched Off Original")
    water_node: bpy.props.BoolProperty(
        name="Water Node")
    highway_bridge: bpy.props.BoolProperty(
        name="Highway Or Bridge")
    switched_off: bpy.props.BoolProperty(
        name="Switched Off")

    # Flags3
    tunnel: bpy.props.BoolProperty(
        name="Tunnel")
    heuretic: bpy.props.IntProperty(
        name="Heuretic")
    
    # Flags4
    density: bpy.props.IntProperty(
        name="Density")
    deadness: bpy.props.IntProperty(
        name="Deadness")
    left_turn_only: bpy.props.BoolProperty(
        name="Left Turn Only")
    
    # Flags5
    has_junction: bpy.props.BoolProperty(
        name="Has Heightmap")
    speed: bpy.props.EnumProperty(
        items=speeds, name="Speed")
    

class LinkFlags(FlagPropertyGroup, bpy.types.PropertyGroup):

    # Flags0
    gps_both_ways: bpy.props.BoolProperty(
        name="GPS Both Ways")
    block_if_no_lanes: bpy.props.BoolProperty(
        name="Block if no lanes")
    tilt: bpy.props.IntProperty(
        name="Tilt")
    tilt_falloff: bpy.props.IntProperty(
        name="Tilt Falloff")
    
    # Flags1
    tilt_falloff_2: bpy.props.BoolProperty(
        name="Tilt Falloff 2")
    narrow_road: bpy.props.BoolProperty(
        name="Narrow Road")
    leads_to_dead_end: bpy.props.BoolProperty(
        name="Leads To Dead End")
    leads_from_dead_end: bpy.props.BoolProperty(
        name="Leads From Dead End")
    negative_offset: bpy.props.BoolProperty(
        name="Negative Offset")
    offset: bpy.props.IntProperty(
        name="Offset")
    
    # Flags2
    dont_use_for_navigation: bpy.props.BoolProperty(
        name="Don't Use For Navigation")
    shortcut: bpy.props.BoolProperty(
        name="Shortcut")
    bwd_lanes: bpy.props.IntProperty(
        name="Bwd Lanes")
    fwd_lanes: bpy.props.IntProperty(
        name="Fwd Lanes")