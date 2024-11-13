import bpy

def create_green_link_material():
    material = bpy.data.materials.new(name="Green Link")
    material.use_nodes = True

    nodes = material.node_tree.nodes
    principled_bsdf = nodes.get("Principled BSDF")
    principled_bsdf.inputs['Base Color'].default_value = (0, 1, 0, 1)
    principled_bsdf.inputs['Alpha'].default_value = 0.5
    material.surface_render_method = 'BLENDED'
    material.diffuse_color = (0, 1, 0, 0.5)




def create_geonode():
    create_green_link_material()
    node_group_name = "StreetGeoNode"

    if node_group_name not in bpy.data.node_groups:

        node_tree = bpy.data.node_groups.new(name=node_group_name, type="GeometryNodeTree")
        node_tree.nodes.clear()

        # Base Nodes
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
            name="Length",
            in_out="INPUT",
            socket_type="NodeSocketFloat"
        )
        node_tree.interface.new_socket(
            name="Geometry",
            in_out="OUTPUT",
            socket_type="NodeSocketGeometry"
        )

        # Add Nodes
        curve_line_node        = node_tree.nodes.new("GeometryNodeCurvePrimitiveLine")
        mesh_line_node         = node_tree.nodes.new("GeometryNodeCurvePrimitiveLine")
        object_info_node       = node_tree.nodes.new("GeometryNodeObjectInfo")
        join_geometry_node     = node_tree.nodes.new("GeometryNodeJoinGeometry")
        curve_to_mesh_node     = node_tree.nodes.new("GeometryNodeCurveToMesh")
        set_material_node      = node_tree.nodes.new("GeometryNodeSetMaterial")
        divide_node            = node_tree.nodes.new("ShaderNodeMath")
        combine_xyz            = node_tree.nodes.new("ShaderNodeCombineXYZ")

        object_info_node.transform_space = "RELATIVE"
        mesh_line_node.mode = "DIRECTION"
        divide_node.operation = "DIVIDE"
        divide_node.inputs[1].default_value = -2
        mesh_line_node.inputs[2].default_value = 1, 0, 0


        # Nodes Placement
        group_in.location             = (-500, 0)
        object_info_node.location     = (-300, 0)
        curve_line_node.location      = (0, 0)
        divide_node.location          = (-300, -300)
        combine_xyz.location          = (0, -300)
        mesh_line_node.location       = (250, -300)
        curve_to_mesh_node.location   = (450, -300)
        set_material_node.location    = (700, -150)
        join_geometry_node.location   = (1000, 0)
        group_out.location            = (1200, 0)

        # Nodes Connections
        node_tree.links.new(group_in.outputs["Geometry"], join_geometry_node.inputs["Geometry"])
        node_tree.links.new(group_in.outputs["Object"], object_info_node.inputs["Object"])
        node_tree.links.new(object_info_node.outputs["Location"], curve_line_node.inputs["End"])
        node_tree.links.new(join_geometry_node.outputs["Geometry"], group_out.inputs["Geometry"])

        node_tree.links.new(group_in.outputs["Material"], set_material_node.inputs["Material"])
        node_tree.links.new(group_in.outputs["Length"], divide_node.inputs[0])
        node_tree.links.new(group_in.outputs["Length"], mesh_line_node.inputs["Length"])

        node_tree.links.new(divide_node.outputs["Value"], combine_xyz.inputs["X"])
        node_tree.links.new(combine_xyz.outputs["Vector"], mesh_line_node.inputs["Start"])
        
        node_tree.links.new(curve_line_node.outputs["Curve"], curve_to_mesh_node.inputs["Curve"])
        node_tree.links.new(mesh_line_node.outputs["Curve"], curve_to_mesh_node.inputs["Profile Curve"])

        node_tree.links.new(curve_to_mesh_node.outputs["Mesh"], set_material_node.inputs["Geometry"])
        node_tree.links.new(set_material_node.outputs["Geometry"], join_geometry_node.inputs["Geometry"])


        return node_tree