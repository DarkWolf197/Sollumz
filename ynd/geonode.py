import bpy

class UpdateGeonode:
    def update_narrow(self, context): #TO FIX (Breaks links on import)
        link_index = context.view_layer.objects.active.node_properties.link_index
        if self.narrow_road:
            bpy.context.object.modifiers[link_index]["Socket_3"] -= 0.7
        else:
            bpy.context.object.modifiers[link_index]["Socket_3"] += 0.7
    
    def update_material(link, obj, to_obj, geonode):
        if obj.node_properties.flags.special_type in ("PED_CROSSING", "PED_ASSISTED", "PED_CROSSING_NOWAIT"):
            geonode["Socket_2"] = add_link_material("Yellow Link", (1, 0.5, 0, 0.5))
            geonode["Socket_3"] = 1.05
        if link.flags.dont_use_for_navigation:
            geonode["Socket_2"] = add_link_material("Magenta Link", (1, 0, 1, 0.5))
            geonode["Socket_3"] = 3.5
        if link.flags.shortcut:
            geonode["Socket_2"] = add_link_material("Cyan Link", (0, 1, 1, 0.5))
            geonode["Socket_3"] = 1.05
        if obj.node_properties.flags.switched_off or (to_obj and to_obj.node_properties.flags.switched_off):
            geonode["Socket_2"] = add_link_material("Disabled Link", (1, 1, 1, 0.35))
            geonode["Socket_3"] = 3.5
        else:
            pass






def add_link_material(name, rgba):
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    
    material = bpy.data.materials.new(name=f"{name}")
    material.use_nodes = True

    nodes = material.node_tree.nodes
    principled_bsdf = nodes.get("Principled BSDF")
    if principled_bsdf:
        principled_bsdf.inputs['Base Color'].default_value = (rgba[0], rgba[1], rgba[2], 1)
        principled_bsdf.inputs['Alpha'].default_value = rgba[3]

    material.blend_method = 'BLEND'
    material.diffuse_color = (rgba[0], rgba[1], rgba[2], rgba[3])

    return material



def apply_geonode(obj, to_obj, link_id):
    geonode = obj.modifiers.new(name="GeometryNodes", type='NODES')
    geonode.node_group = bpy.data.node_groups["StreetGeoNode"]
    geonode.name = f"Link {link_id}"
    geonode["Socket_1"] = to_obj
    geonode["Socket_2"] = add_link_material("Green Link", (0, 1, 0, 0.5))
    geonode["Socket_3"] = 7

    links = obj.node_properties.links
    for link in links:
        UpdateGeonode.update_material(link, obj, to_obj, geonode)

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

        set_red_material_node.inputs[2].default_value = add_link_material("Red Line", (1, 0, 0, 1))

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