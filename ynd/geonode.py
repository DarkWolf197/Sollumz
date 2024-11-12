import bpy

def create_geonode():

    node_group_name = "StreetGeoNode"

    if node_group_name not in bpy.data.node_groups:

        node_tree = bpy.data.node_groups.new(name=node_group_name, type='GeometryNodeTree')
        
        # Pulisci i nodi esistenti
        node_tree.nodes.clear()

        # Aggiungi i nodi base
        group_in = node_tree.nodes.new('NodeGroupInput')
        group_out = node_tree.nodes.new('NodeGroupOutput')

        # Creiamo i socket necessari nell'interfaccia
        node_tree.interface.clear()
        # Input socket per la geometria
        node_tree.interface.new_socket(
            name="Geometry",
            in_out='INPUT',
            socket_type='NodeSocketGeometry'
        )
        # Input socket per l'oggetto
        node_tree.interface.new_socket(
            name="Object",
            in_out='INPUT',
            socket_type='NodeSocketObject'
        )
        # Output socket per la geometria finale
        node_tree.interface.new_socket(
            name="Geometry",
            in_out='OUTPUT',
            socket_type='NodeSocketGeometry'
        )

        # Aggiungi i nodi specifici
        curve_line_node = node_tree.nodes.new('GeometryNodeCurvePrimitiveLine')
        object_info_node = node_tree.nodes.new('GeometryNodeObjectInfo')
        join_geometry_node = node_tree.nodes.new('GeometryNodeJoinGeometry')

        object_info_node.transform_space = 'RELATIVE'

        # Posiziona i nodi
        group_in.location           = (-500, 0)
        object_info_node.location   = (-300, 0)
        curve_line_node.location    = (0, 0)
        join_geometry_node.location = (300, 0)
        group_out.location          = (500, 0)

        node_tree.links.new(group_in.outputs[0], join_geometry_node.inputs[0])
        node_tree.links.new(group_in.outputs[1], object_info_node.inputs[0])
        node_tree.links.new(object_info_node.outputs[1], curve_line_node.inputs[1])
        node_tree.links.new(curve_line_node.outputs["Curve"], join_geometry_node.inputs["Geometry"])
        node_tree.links.new(join_geometry_node.outputs["Geometry"], group_out.inputs["Geometry"])

        return node_tree