import bpy

def find_node(area_id, node_id):
    for obj in bpy.context.scene.objects:
        if (obj.node_properties.area_id, obj.node_properties.node_id) == (area_id, node_id):
            return obj
    return None


def is_ped_node(specialType):
    return specialType in ["PED_CROSSING", "PED_ASSISTED", "PED_CROSSING_NOWAIT"]


def get_lane_width(link, node1, node2):
    if link.shortcut or is_ped_node(node1.node_properties.flags.special_type) or (node2 and is_ped_node(node2.node_properties.flags.special_type)):
        return 0.5
    if link.dont_use_for_navigation:
        return 2.5
    if link.narrow_road:
        return 4.0
    return 5.5


def get_colour(link, node1, node2):

    node1_flags = node1.node_properties.flags
    node2_flags = node2.node_properties.flags if node2 else None

    def is_switched_off(node_flags):
        return node_flags.switched_off_original or node_flags.switched_off
    #--------------------------------------------------------------------#
    if link.shortcut:
        return [0.0, 0.2, 0.2, 0.5]

    if is_switched_off(node1_flags) or (node2_flags and is_switched_off(node2_flags)):
        if node1_flags.offroad or (node2_flags and node2_flags.offroad):
            return [0.0196, 0.0156, 0.0043, 0.5]
        return [0.02, 0.0, 0.0, 0.5]

    if is_ped_node(node1_flags.special_type) or (node2 and is_ped_node(node2_flags.special_type)):
        return [0.2, 0.15, 0.0, 0.5]

    if node1_flags.offroad or (node2_flags and node2_flags.offroad):
        return [0.196, 0.156, 0.043, 0.5]

    if link.dont_use_for_navigation:
        return [0.2, 0.0, 0.2, 0.5]

    return [0.0, 0.2, 0.0, 0.5]

