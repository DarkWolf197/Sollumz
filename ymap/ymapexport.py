import bpy
import re
import math
import numpy as np
from mathutils import Vector
from struct import pack
from ..cwxml.ymap import *
from binascii import hexlify
from ..tools.blenderhelper import remove_number_suffix
from ..tools.meshhelper import get_bound_center_from_bounds, get_extents
from ..sollumz_properties import SOLLUMZ_UI_NAMES, SollumType
from ..sollumz_preferences import get_export_settings
from .. import logger
from ..tools.ymaphelper import generate_ymap_extents


def box_from_obj(obj):
    box = BoxOccluder()

    bbmin, bbmax = get_extents(obj)
    center = get_bound_center_from_bounds(bbmin, bbmax)
    dimensions = obj.dimensions

    box.center_x = round(center.x * 4)
    box.center_y = round(center.y * 4)
    box.center_z = round(center.z * 4)

    box.length = round(dimensions.x * 4)
    box.width = round(dimensions.y * 4)
    box.height = round(dimensions.z * 4)

    dir = Vector((1, 0, 0))
    dir.rotate(obj.rotation_euler)
    dir *= 0.5
    box.sin_z = round(dir.x * 32767)
    box.cos_z = round(dir.y * 32767)

    return box


def triangulate_obj(obj):
    """Convert mesh from n-polygons to triangles"""
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.quads_convert_to_tris()
    bpy.ops.object.mode_set(mode="OBJECT")


def occlusion_model_obj_get_data_buffer(obj) -> bytes:
    """
    For each vertex get its coordinates in global space (this way we don't need to apply transfroms) as 32-bit floats
    and for each face get its indices as 8-bit integers. Then convert them to bytes and append them together.

    :return verts: Bytes buffer containing the vertex coordinates and face indices
    :rtype bytes:
    """
    # TODO: should validate that the mesh is within <256 verts
    mesh = obj.data
    verts = np.array([obj.matrix_world @ v.co for v in mesh.vertices], dtype=np.float32)
    indices = np.array([i for p in mesh.polygons for i in p.vertices], dtype=np.uint8)
    return verts.tobytes() + indices.tobytes()


def model_from_obj(obj):
    triangulate_obj(obj)

    model = OccludeModel()
    model.bmin, model.bmax = get_extents(obj)
    model.verts = occlusion_model_obj_get_data_buffer(obj)
    model.num_verts_in_bytes = len(obj.data.vertices) * 12
    face_count = len(obj.data.polygons)
    model.num_tris = face_count | 0x8000  # add float vertex format marker
    model.data_size = len(model.verts)
    model.flags = obj.ymap_model_occl_properties.model_occl_flags

    assert model.data_size == (model.num_verts_in_bytes + face_count * 3)

    return model


def entity_from_obj(obj):
    # Removing " (not found)" suffix, created when importing ymaps while entity was not found in the view layer
    obj.name = re.sub(" \(not found\)", "", obj.name.lower())

    entity = Entity()
    entity.archetype_name = remove_number_suffix(obj.name)
    entity.flags = int(obj.entity_properties.flags)
    entity.guid = int(obj.entity_properties.guid)
    entity.position = obj.location
    entity.rotation = obj.rotation_euler.to_quaternion()
    if entity.type != "CMloInstanceDef":
        entity.rotation.invert()
    entity.scale_xy = obj.scale.x
    entity.scale_z = obj.scale.z
    entity.parent_index = int(obj.entity_properties.parent_index)
    entity.lod_dist = obj.entity_properties.lod_dist
    entity.child_lod_dist = obj.entity_properties.child_lod_dist
    entity.lod_level = obj.entity_properties.lod_level.upper().replace("SOLLUMZ_", "")
    entity.num_children = int(obj.entity_properties.num_children)
    entity.priority_level = obj.entity_properties.priority_level.upper().replace("SOLLUMZ_", "")
    entity.ambient_occlusion_multiplier = int(
        obj.entity_properties.ambient_occlusion_multiplier)
    entity.artificial_ambient_occlusion = int(
        obj.entity_properties.artificial_ambient_occlusion)
    entity.tint_value = int(obj.entity_properties.tint_value)

    return entity

def cargen_from_obj(obj):
    cargen = CarGenerator()
    cargen.position = obj.location

    cargen.orient_x, cargen.orient_y = calculate_cargen_orient(obj)

    cargen.perpendicular_length = obj.ymap_cargen_properties.perpendicular_length
    cargen.car_model = obj.ymap_cargen_properties.car_model
    cargen.flags = obj.ymap_cargen_properties.cargen_flags
    cargen.body_color_remap_1 = obj.ymap_cargen_properties.body_color_remap_1
    cargen.body_color_remap_2 = obj.ymap_cargen_properties.body_color_remap_2
    cargen.body_color_remap_3 = obj.ymap_cargen_properties.body_color_remap_3
    cargen.body_color_remap_4 = obj.ymap_cargen_properties.body_color_remap_4
    cargen.pop_group = obj.ymap_cargen_properties.pop_group
    cargen.livery = obj.ymap_cargen_properties.livery

    return cargen


def calculate_cargen_orient(obj):
    # *-1 because GTA likes to invert values
    angle = obj.rotation_euler[2] * -1

    return 5 * math.sin(angle), 5 * math.cos(angle)

def quantize_position(real_pos, bounds_min, bounds_max):
    def quantize(val, min_val, max_val):
        # Evita divisioni per zero
        if max_val == min_val:
            return 0
        norm = (val - min_val) / (max_val - min_val)
        return max(0, min(65535, int(round(norm * 65535))))

    qx = quantize(real_pos.x, bounds_min.x, bounds_max.x)
    qy = quantize(real_pos.y, bounds_min.y, bounds_max.y)
    qz = quantize(real_pos.z, bounds_min.z, bounds_max.z)

    return f"{qx} {qy} {qz}"


def encode_normal(x, y, z):
    length = math.sqrt(x * x + y * y + z * z)
    if length == 0:
        x, y, z = 0.0, 0.0, 1.0

    # Step 2: Ricodifica X e Y in valori interi 0-255
    normal_x = int(round(((x + 1.0) / 2.0) * 255))
    normal_y = int(round(((y + 1.0) / 2.0) * 255))

    # Clamp per sicurezza
    normal_x = max(0, min(255, normal_x))
    normal_y = max(0, min(255, normal_y))
    
    return normal_x, normal_y

import mathutils

def get_batch_extents(batch_obj):
    bbox_min = mathutils.Vector((float('inf'), float('inf'), float('inf')))
    bbox_max = mathutils.Vector((float('-inf'), float('-inf'), float('-inf')))

    for child in batch_obj.children:
        world_bbox = [child.matrix_world @ mathutils.Vector(corner) for corner in child.bound_box]

        for v in world_bbox:
            bbox_min.x = min(bbox_min.x, v.x - 0.4)
            bbox_min.y = min(bbox_min.y, v.y - 0.4)
            bbox_min.z = min(bbox_min.z, v.z - 0.4)

            bbox_max.x = max(bbox_max.x, v.x + 0.4)
            bbox_max.y = max(bbox_max.y, v.y + 0.4)
            bbox_max.z = max(bbox_max.z, v.z + 0.4)

    return bbox_min, bbox_max


def ymap_from_object(obj):
    ymap = CMapData()

    export_settings = get_export_settings()

    for child in obj.children:
        # Entities
        if export_settings.ymap_exclude_entities == False and child.sollum_type == SollumType.YMAP_ENTITY_GROUP:
            for entity_obj in child.children:
                ymap.entities.append(entity_from_obj(entity_obj))

        # Box occluders
        if export_settings.ymap_box_occluders == False and child.sollum_type == SollumType.YMAP_BOX_OCCLUDER_GROUP:
            obj.ymap_properties.content_flags_toggle.has_occl = True

            for box_obj in child.children:
                rotation = box_obj.rotation_euler
                if abs(rotation.x) > 0.01 or abs(rotation.y) > 0.01:
                    logger.error(
                        f"Box occluders only support Z-axis rotation. Skipping {box_obj.name} due to X/Y rotation.")
                    continue

                if box_obj.sollum_type == SollumType.YMAP_BOX_OCCLUDER:
                    ymap.box_occluders.append(box_from_obj(box_obj))
                else:
                    logger.warning(
                        f"Object {box_obj.name} will be skipped because it is not a {SOLLUMZ_UI_NAMES[SollumType.YMAP_BOX_OCCLUDER]} type.")

        # Model occluders
        if export_settings.ymap_model_occluders == False and child.sollum_type == SollumType.YMAP_MODEL_OCCLUDER_GROUP:
            obj.ymap_properties.content_flags_toggle.has_occl = True

            for model_obj in child.children:
                if model_obj.sollum_type == SollumType.YMAP_MODEL_OCCLUDER:
                    if len(model_obj.data.vertices) > 256:
                        logger.warning(
                            f"Object {model_obj.name} has too many vertices and will be skipped. It can not have more than 256 vertices.")
                        continue

                    ymap.occlude_models.append(
                        model_from_obj(model_obj))
                else:
                    logger.warning(
                        f"Object {model_obj.name} will be skipped because it is not a {SOLLUMZ_UI_NAMES[SollumType.YMAP_MODEL_OCCLUDER]} type.")


        for physic_dict in obj.ymap_properties.phyiscs_dict:
            for physic_obj in child.children:
                    physic = PhysicsDictionariesList.PhysicsDictionarie()
                    physic.value = physic_dict.name
                    ymap.physics_dictionaries.append(physic)


        if child.sollum_type == SollumType.GRASS_GROUP:
            instanced_data = InstancedDataProperty()

            batches = []
            for batch in child.children:
                bbox_min, bbox_max = get_batch_extents(batch)

                instances = []
                for grass_obj in batch.children:
                    norm_x, norm_y = encode_normal(
                        grass_obj.rotation_euler.x,
                        grass_obj.rotation_euler.y,
                        grass_obj.rotation_euler.z
                    )
                    grass_instance = GrassInstance()
                    grass_instance.position = quantize_position(
                        grass_obj.location,
                        bbox_min, bbox_max
                    )
                    grass_instance.normal_x = norm_x
                    grass_instance.normal_y = norm_y
                    grass_instance.color = grass_obj.ymap_grass_inst_properties.color
                    grass_instance.scale = grass_obj.ymap_grass_inst_properties.scale
                    grass_instance.ao = grass_obj.ymap_grass_inst_properties.ao
                    grass_instance.pad = grass_obj.ymap_grass_inst_properties.pad
                    instances.append(grass_instance)

                bbox = BatchAABB()
                bbox.min=Vector((bbox_min.x, bbox_min.y, bbox_min.z, 0))
                bbox.max=Vector((bbox_max.x, bbox_max.y, bbox_max.z, 0))
                
                batch_instance = GrassInstanceBatch()
                batch_instance.batch_aabb = bbox
                batch_instance.scale_range = batch.ymap_grass_batch_properties.scale_range
                batch_instance.archetype_name = batch.name
                batch_instance.lod_dist = batch.ymap_grass_batch_properties.lod_dist
                batch_instance.lod_fade_start_dist = batch.ymap_grass_batch_properties.lod_fade_start_dist
                batch_instance.lod_inst_fade_range = batch.ymap_grass_batch_properties.lod_inst_fade_range
                batch_instance.orient_to_terrain = batch.ymap_grass_batch_properties.orient_to_terrain
                batch_instance.instance_list = instances
                batches.append(batch_instance)
            instanced_data.grass_instance_list = batches


        # Car generators
        if export_settings.ymap_car_generators == False and child.sollum_type == SollumType.YMAP_CAR_GENERATOR_GROUP:
            for cargen_obj in child.children:
                rotation = cargen_obj.rotation_euler
                if abs(rotation.x) > 0.01 or abs(rotation.y) > 0.01:
                    logger.error(
                        f"Car generators only support Z-axis rotation. Skipping {cargen_obj.name} due to X/Y rotation.")
                    continue
                if cargen_obj.sollum_type == SollumType.YMAP_CAR_GENERATOR:
                    ymap.car_generators.append(cargen_from_obj(cargen_obj))
                else:
                    logger.warning(
                        f"Object {cargen_obj.name} will be skipped because it is not a {SOLLUMZ_UI_NAMES[SollumType.YMAP_CAR_GENERATOR]} type.")

        # TODO: lod ligths

        # TODO: distant lod lights

    ymap.name = remove_number_suffix(obj.name)
    ymap.parent = obj.ymap_properties.parent
    ymap.flags = obj.ymap_properties.flags
    ymap.content_flags = obj.ymap_properties.content_flags
    ymap.instanced_data = instanced_data if 'instanced_data' in locals() else None

    generate_ymap_extents(obj)
    ymap.entities_extents_min = obj.ymap_properties.entities_extents_min
    ymap.entities_extents_max = obj.ymap_properties.entities_extents_max
    ymap.streaming_extents_min = obj.ymap_properties.streaming_extents_min
    ymap.streaming_extents_max = obj.ymap_properties.streaming_extents_max

    ymap.block.version = obj.ymap_properties.block.version
    ymap.block.flags = obj.ymap_properties.block.flags
    ymap.block.name = obj.ymap_properties.block.name
    ymap.block.exported_by = obj.ymap_properties.block.exported_by
    ymap.block.owner = obj.ymap_properties.block.owner
    ymap.block.time = obj.ymap_properties.block.time

    return ymap


def export_ymap(obj: bpy.types.Object, filepath: str) -> bool:
    ymap = ymap_from_object(obj)
    ymap.write_xml(filepath)
    return True
