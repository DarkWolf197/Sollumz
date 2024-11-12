import bpy

def find_node(area_id, node_id):
    for obj in bpy.context.scene.objects:
        if (obj.node_properties.area_id, obj.node_properties.node_id) == (area_id, node_id):
            return obj