import bpy
from ..sollumz_properties import SollumType
from .. import logger

def create_materials(mat_name, color):

    mat = bpy.data.materials.get(mat_name)

    if not mat:
        alpha = 0.8
        mat = bpy.data.materials.new(mat_name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        principled_bsdf = nodes.get("Principled BSDF")
        principled_bsdf.inputs['Base Color'].default_value = (color[0], color[1], color[2], alpha)
        principled_bsdf.inputs['Alpha'].default_value = alpha

        material_output = mat.node_tree.nodes.get('Material Output')

        mat.node_tree.links.new(material_output.inputs[0], principled_bsdf.outputs[0])
        mat.diffuse_color = (color[0], color[1], color[2], alpha)

    return mat


def ensure_quad_data(quad):
    mesh = quad.data
    global_coords = [quad.matrix_world @ vert.co for vert in mesh.vertices]

    minX = min(coord.x for coord in global_coords)
    maxX = max(coord.x for coord in global_coords)
    minY = min(coord.y for coord in global_coords)
    maxY = max(coord.y for coord in global_coords)

    expected_vertices = {
        (minX, minY),
        (maxX, minY),
        (maxX, maxY),
        (minX, maxY)}
    
    actual_vertices = {(coord.x, coord.y) for coord in global_coords}

    if expected_vertices != actual_vertices:
        logger.warning(f"Object {quad.name} will be skipped because is not uniform. (Vertices)")
        return None

    if quad.sollum_type == SollumType.WATER_QUAD:
        z = global_coords[0].z
        z_values = [coord.z for coord in global_coords]
        if not all(z == z_values[0] for z in z_values): 
            logger.warning(f"Object {quad.name} will be skipped because is not uniform. (Height)")
            return None

        return minX, maxX, minY, maxY, z
    
    return minX, maxX, minY, maxY