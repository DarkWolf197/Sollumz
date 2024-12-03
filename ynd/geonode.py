import bpy
from .utils import get_lane_width, get_colour


def update_material(link, obj, to_obj, geonode):
    geonode["Socket_2"] = add_link_material(get_colour(link.flags, obj, to_obj))
    geonode["Socket_3"] = get_lane_width(link.flags, obj, to_obj)


def add_link_material(rgba):
    unique_name = f"LINKMAT_{rgba[0]:.3f}.{rgba[1]:.3f}.{rgba[2]:.3f}.{rgba[3]:.3f}"
    
    if unique_name in bpy.data.materials:
        return bpy.data.materials[unique_name]
    
    material = bpy.data.materials.new(name=unique_name)
    material.use_nodes = True

    nodes = material.node_tree.nodes
    principled_bsdf = nodes.get("Principled BSDF")
    if principled_bsdf:
        principled_bsdf.inputs['Base Color'].default_value = (rgba[0], rgba[1], rgba[2], 1)
        principled_bsdf.inputs['Alpha'].default_value = rgba[3]

    material.blend_method = 'BLEND'
    material.diffuse_color = (rgba[0], rgba[1], rgba[2], rgba[3])

    return material


def apply_geonode(obj, to_obj):

    if to_obj:
        for mod in to_obj.modifiers:
            if mod.type == 'NODES' and mod.node_group is not None:
                if mod.get("Socket_1") == obj:
                    return

        geonode = obj.modifiers.new(name="GeometryNodes", type='NODES')
        geonode.node_group = bpy.data.node_groups["StreetGeoNode"]
        geonode.name = "Link"
        geonode["Socket_1"] = to_obj

        links = obj.node_properties.links
        for link in links:
            update_material(link, obj, to_obj, geonode)


def create_geonode():
    node_group_name = "StreetGeoNode"

    if node_group_name not in bpy.data.node_groups:

        node_tree = bpy.data.node_groups.new(name=node_group_name, type="GeometryNodeTree")
        node_tree.nodes.clear()

    # Sockets
        group_in = node_tree.nodes.new("NodeGroupInput")
        group_out = node_tree.nodes.new("NodeGroupOutput")

        node_tree.interface.clear()

        node_tree.interface.new_socket(
            name="Geometry",
            in_out="INPUT",
            socket_type="NodeSocketGeometry"
        )
        node_tree.interface.new_socket(
            name="Object",
            in_out="INPUT",
            socket_type="NodeSocketObject"
        )
        node_tree.interface.new_socket(
            name="Material",
            in_out="INPUT",
            socket_type="NodeSocketMaterial"
        )
        node_tree.interface.new_socket(
            name="Width",
            in_out="INPUT",
            socket_type="NodeSocketFloat"
        )
        node_tree.interface.new_socket(
            name="Geometry",
            in_out="OUTPUT",
            socket_type="NodeSocketGeometry"
        )

    # Add Nodes
        object_info_node       = node_tree.nodes.new("GeometryNodeObjectInfo")

        curve_line_node        = node_tree.nodes.new("GeometryNodeCurvePrimitiveLine")
        curve_circle_node      = node_tree.nodes.new("GeometryNodeCurvePrimitiveCircle")
        red_curve_to_mesh_node = node_tree.nodes.new("GeometryNodeCurveToMesh")
        set_red_material_node  = node_tree.nodes.new("GeometryNodeSetMaterial")

        quadrilateral_node     = node_tree.nodes.new("GeometryNodeCurvePrimitiveQuadrilateral")
        curve_to_mesh_node     = node_tree.nodes.new("GeometryNodeCurveToMesh")
        dup_element_node       = node_tree.nodes.new("GeometryNodeDuplicateElements")
        set_positon_node       = node_tree.nodes.new("GeometryNodeSetPosition")
        set_material_node      = node_tree.nodes.new("GeometryNodeSetMaterial")

        vector_sub = node_tree.nodes.new("ShaderNodeVectorMath")
        vector_sub.operation = 'SUBTRACT'
        vector_norm = node_tree.nodes.new("ShaderNodeVectorMath")
        vector_norm.operation = 'NORMALIZE'
        vector_cross = node_tree.nodes.new("ShaderNodeVectorMath")
        vector_cross.operation = 'CROSS_PRODUCT'
        vector_scale = node_tree.nodes.new("ShaderNodeVectorMath")
        vector_scale.operation = 'SCALE'

        join_geometry_node     = node_tree.nodes.new("GeometryNodeJoinGeometry")

    # Node Properties
        object_info_node.transform_space = "RELATIVE"
        quadrilateral_node.inputs[1].default_value = 0

        curve_circle_node.inputs[0].default_value = 3
        curve_circle_node.inputs[4].default_value = 0.02

        set_red_material_node.inputs[2].default_value = add_link_material((1, 0, 0, 1))

        dup_element_node.domain = 'FACE'

    # Nodes Placement
        group_in.location             = (-500, 0)

        object_info_node.location     = (-300, 0)
        curve_line_node.location      = (-100, 0)
        curve_circle_node.location    = (250, 150)
        red_curve_to_mesh_node.location = (500, 150)
        set_red_material_node.location = (750, 150)

        quadrilateral_node.location   = (-100, -200)
        curve_to_mesh_node.location   = (250, -200)
        set_positon_node.location     = (500, -200)
        set_material_node.location    = (700, -200)

        vector_sub.location           = (-100, -400)
        vector_norm.location          = (50, -400)
        vector_cross.location         = (200, -400)
        vector_scale.location         = (350, -400)

        join_geometry_node.location   = (1000, 0)
        group_out.location            = (1200, 0)

    # Nodes Connections

        # Starter Nodes
        node_tree.links.new(group_in.outputs["Geometry"], join_geometry_node.inputs["Geometry"])
        node_tree.links.new(group_in.outputs["Object"], object_info_node.inputs["Object"])
        node_tree.links.new(group_in.outputs["Material"], set_material_node.inputs["Material"])
        node_tree.links.new(object_info_node.outputs["Location"], curve_line_node.inputs["End"])

        # Curve Main Outputs
        node_tree.links.new(curve_line_node.outputs["Curve"], curve_to_mesh_node.inputs["Curve"])
        node_tree.links.new(curve_line_node.outputs["Curve"], red_curve_to_mesh_node.inputs["Curve"])

        # Red Line (Up)
        node_tree.links.new(curve_circle_node.outputs["Curve"], red_curve_to_mesh_node.inputs["Profile Curve"])
        node_tree.links.new(red_curve_to_mesh_node.outputs["Mesh"], set_red_material_node.inputs["Geometry"])
        node_tree.links.new(set_red_material_node.outputs["Geometry"], join_geometry_node.inputs["Geometry"])

        # Street Mesh (Middle)
        node_tree.links.new(group_in.outputs["Width"], quadrilateral_node.inputs["Width"])
        node_tree.links.new(quadrilateral_node.outputs["Curve"], curve_to_mesh_node.inputs["Profile Curve"])
        node_tree.links.new(join_geometry_node.outputs["Geometry"], group_out.inputs["Geometry"])
        node_tree.links.new(curve_to_mesh_node.outputs["Mesh"], dup_element_node.inputs["Geometry"])
        node_tree.links.new(dup_element_node.outputs["Geometry"], set_positon_node.inputs["Geometry"])
        node_tree.links.new(set_positon_node.outputs["Geometry"], set_material_node.inputs["Geometry"])
        node_tree.links.new(set_material_node.outputs["Geometry"], join_geometry_node.inputs["Geometry"])

        # Street Offset (Lower)
        node_tree.links.new(object_info_node.outputs["Location"], vector_sub.inputs[1])
        node_tree.links.new(vector_sub.outputs["Vector"], vector_norm.inputs["Vector"])
        node_tree.links.new(vector_norm.outputs["Vector"], vector_cross.inputs[0])
        node_tree.links.new(vector_cross.outputs["Vector"], vector_scale.inputs["Vector"])
        node_tree.links.new(vector_scale.outputs["Vector"], set_positon_node.inputs["Offset"])

        return node_tree