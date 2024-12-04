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
            name="Linked",
            in_out="INPUT",
            socket_type="NodeSocketObject"
        )
        node_tree.interface.new_socket(
            name="Color",
            in_out="INPUT",
            socket_type="NodeSocketMaterial"
        )
        node_tree.interface.new_socket(
            name="Width",
            in_out="INPUT",
            socket_type="NodeSocketFloat"
        )
        node_tree.interface.new_socket(
            name="Negative Offset",
            in_out="INPUT",
            socket_type="NodeSocketBool"
        )
        node_tree.interface.new_socket(
            name="Offset",
            in_out="INPUT",
            socket_type="NodeSocketInt"
        )

        node_tree.interface.new_socket(
            name="Geometry",
            in_out="OUTPUT",
            socket_type="NodeSocketGeometry"
        )

    # Add Nodes
        object_info = node_tree.nodes.new("GeometryNodeObjectInfo")
        object_info.transform_space = "RELATIVE"

        curve_line = node_tree.nodes.new("GeometryNodeCurvePrimitiveLine")
        curve_circle = node_tree.nodes.new("GeometryNodeCurvePrimitiveCircle")
        curve_circle.inputs[0].default_value = 3
        curve_circle.inputs[4].default_value = 0.02
        red_curve_to_mesh = node_tree.nodes.new("GeometryNodeCurveToMesh")
        set_red_material = node_tree.nodes.new("GeometryNodeSetMaterial")
        set_red_material.inputs[2].default_value = add_link_material((1, 0, 0, 1))

        quadrilateral = node_tree.nodes.new("GeometryNodeCurvePrimitiveQuadrilateral")
        quadrilateral.inputs[1].default_value = 0
        curve_to_mesh = node_tree.nodes.new("GeometryNodeCurveToMesh")
        dup_element = node_tree.nodes.new("GeometryNodeDuplicateElements")
        dup_element.domain = 'FACE'
        set_positon = node_tree.nodes.new("GeometryNodeSetPosition")
        set_material = node_tree.nodes.new("GeometryNodeSetMaterial")
        offset_idx_swtc = node_tree.nodes.new("GeometryNodeIndexSwitch")
        offset_idx_swtc.data_type = 'INT'
        offset_idx_swtc.location = (-300, -800)
        offset_idx_swtc.inputs[1].default_value = 1
        offset_idx_swtc.inputs[2].default_value = -1
        offset_math_mult = node_tree.nodes.new("ShaderNodeMath")
        offset_math_mult.operation = 'MULTIPLY'
        offset_math_mult.location = (-150, -800)
        offset_math_div = node_tree.nodes.new("ShaderNodeMath")
        offset_math_div.operation = 'DIVIDE'
        offset_math_div.location = (0, -800)
        offset_math_div.inputs[1].default_value = 2.55
        offset_comb_xyz = node_tree.nodes.new("ShaderNodeCombineXYZ")
        offset_comb_xyz.location = (150, -710)
        offset_vec_sub = node_tree.nodes.new("ShaderNodeVectorMath")
        offset_vec_sub.operation = 'SUBTRACT'
        offset_vec_sub.location = (0, -600)
        offset_vec_norm = node_tree.nodes.new("ShaderNodeVectorMath")
        offset_vec_norm.operation = 'NORMALIZE'
        offset_vec_norm.location = (150, -600)
        offset_vec_cross = node_tree.nodes.new("ShaderNodeVectorMath")
        offset_vec_cross.operation = 'CROSS_PRODUCT'
        offset_vec_cross.location = (300, -600)
        offset_vec_scale = node_tree.nodes.new("ShaderNodeVectorMath")
        offset_vec_scale.operation = 'SCALE'
        offset_vec_scale.location = (450, -600)




        join_geometry = node_tree.nodes.new("GeometryNodeJoinGeometry")
        join_geometry.location   = (1000, 0)

    # Nodes Placement
        group_in.location             = (-500, 0)

        object_info.location     = (-300, 0)
        curve_line.location      = (-100, 0)
        curve_circle.location    = (250, 150)
        red_curve_to_mesh.location = (500, 150)
        set_red_material.location = (750, 150)

        quadrilateral.location   = (-100, -200)
        curve_to_mesh.location   = (250, -200)
        set_positon.location     = (500, -200)
        set_material.location    = (700, -200)

        group_out.location            = (1200, 0)
        

    # Nodes Connections

        # Starter Nodes
        node_tree.links.new(group_in.outputs["Geometry"], join_geometry.inputs["Geometry"])
        node_tree.links.new(group_in.outputs["Linked"], object_info.inputs["Object"])
        node_tree.links.new(group_in.outputs["Color"], set_material.inputs["Material"])
        node_tree.links.new(object_info.outputs["Location"], curve_line.inputs["End"])

        # Curve Main Outputs
        node_tree.links.new(curve_line.outputs["Curve"], curve_to_mesh.inputs["Curve"])
        node_tree.links.new(curve_line.outputs["Curve"], red_curve_to_mesh.inputs["Curve"])

        # Red Line
        node_tree.links.new(curve_circle.outputs["Curve"], red_curve_to_mesh.inputs["Profile Curve"])
        node_tree.links.new(red_curve_to_mesh.outputs["Mesh"], set_red_material.inputs["Geometry"])
        node_tree.links.new(set_red_material.outputs["Geometry"], join_geometry.inputs["Geometry"])

        # Street Mesh
        node_tree.links.new(group_in.outputs["Width"], quadrilateral.inputs["Width"])
        node_tree.links.new(quadrilateral.outputs["Curve"], curve_to_mesh.inputs["Profile Curve"])
        node_tree.links.new(join_geometry.outputs["Geometry"], group_out.inputs["Geometry"])
        node_tree.links.new(curve_to_mesh.outputs["Mesh"], dup_element.inputs["Geometry"])
        node_tree.links.new(dup_element.outputs["Geometry"], set_positon.inputs["Geometry"])
        node_tree.links.new(set_positon.outputs["Geometry"], set_material.inputs["Geometry"])
        node_tree.links.new(set_material.outputs["Geometry"], join_geometry.inputs["Geometry"])

        # Street Offset
        node_tree.links.new(group_in.outputs["Negative Offset"], offset_idx_swtc.inputs["Index"])
        node_tree.links.new(group_in.outputs["Offset"], offset_math_mult.inputs[0])
        node_tree.links.new(offset_idx_swtc.outputs["Output"], offset_math_mult.inputs[1])
        node_tree.links.new(offset_math_mult.outputs["Value"], offset_math_div.inputs[0])
        node_tree.links.new(offset_math_div.outputs["Value"], offset_comb_xyz.inputs["Z"])
        node_tree.links.new(offset_comb_xyz.outputs["Vector"], offset_vec_cross.inputs[1])
        
        node_tree.links.new(object_info.outputs["Location"], offset_vec_sub.inputs[1])
        node_tree.links.new(offset_vec_sub.outputs["Vector"], offset_vec_norm.inputs["Vector"])
        node_tree.links.new(offset_vec_norm.outputs["Vector"], offset_vec_cross.inputs[0])
        node_tree.links.new(offset_vec_cross.outputs["Vector"], offset_vec_scale.inputs["Vector"])
        node_tree.links.new(offset_vec_scale.outputs["Vector"], set_positon.inputs["Offset"])

        return node_tree