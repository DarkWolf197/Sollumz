import bpy
from ..sollumz_properties import SollumType, SOLLUMZ_UI_NAMES
from .. import logger

def create_quad_materials():

    mat_data = [
        (SOLLUMZ_UI_NAMES[SollumType.WATER_QUAD],   (0.0, 0.18, 1.0, 1.0)),
        (SOLLUMZ_UI_NAMES[SollumType.CALMING_QUAD], (0.0, 0.66, 1.0, 0.3)),
        (SOLLUMZ_UI_NAMES[SollumType.WAVE_QUAD],    (0.0, 1.00, 0.4, 0.3)),
    ]

    water_mat = bpy.data.materials.new(mat_data[0][0])
    water_mat.diffuse_color = mat_data[0][1]

    calming_mat = bpy.data.materials.new(mat_data[1][0])
    calming_mat.diffuse_color = mat_data[1][1]

    wave_mat = bpy.data.materials.new(mat_data[2][0])
    wave_mat.diffuse_color = mat_data[2][1]

    return water_mat, calming_mat, wave_mat


def is_valid_quad(obj):
    mesh = obj.data
    vertices = [v.co for v in mesh.vertices]
    
    z_set = {round(v.z, 6) for v in vertices}
    if len(z_set) != 1:
        return False

    for v in vertices:
        if not (float(v.x).is_integer() and float(v.y).is_integer()):
            return False

    x_set = {round(v.x, 6) for v in vertices}
    y_set = {round(v.y, 6) for v in vertices}

    if len(x_set) != 2 or len(y_set) != 2:
        return False
    return True


def round_quad(obj):
    mesh = obj.data
    matrix_world_inv = obj.matrix_world.inverted()

    for vert in mesh.vertices:
        global_coord = obj.matrix_world @ vert.co
        if not global_coord.x.is_integer() or not global_coord.y.is_integer():
            global_coord.x = round(global_coord.x)
            global_coord.y = round(global_coord.y)
            global_coord.z = 0.0 if obj.sollum_type in [SollumType.CALMING_QUAD, SollumType.WAVE_QUAD] else global_coord.z
            vert.co = matrix_world_inv @ global_coord

    mesh.update()


def ensure_quad_data(obj):
    if not is_valid_quad(obj):
        
        logger.error(f"{obj.name} failed, try rounding the vertices.")
        round_quad(obj)
        logger.warning(f"Object {obj.name} has been rounded. (Vertices)")
        if not is_valid_quad(obj):
            logger.error(f"Object {obj.name} will be skipped because is not uniform.")
            return False
        return True
    return True
