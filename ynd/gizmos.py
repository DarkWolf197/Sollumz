import bpy
from mathutils import Vector
from ..sollumz_properties import SollumType
from .properties import LinkProperties


class YndBoundsGizmo(bpy.types.Gizmo):
    bl_idname = "OBJECT_GT_node_bounds"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ynd_obj = None

    @staticmethod
    def get_verts(ynd_obj: bpy.types.Object):
        x = ynd_obj.node_dictionary_properties.x
        y = ynd_obj.node_dictionary_properties.y

        center_x = x * 512 - 7936
        center_y = y * 512 - 7936

        min_x = center_x - 512 / 2
        max_x = center_x + 512 / 2
        min_y = center_y - 512 / 2
        max_y = center_y + 512 / 2

        min_z = 0
        max_z = 0
        if ynd_obj.children:
            min_z = min(child.location.z for child in ynd_obj.children)
            max_z = max(child.location.z for child in ynd_obj.children)

        v0 = Vector((min_x, min_y, min_z))
        v1 = Vector((max_x, min_y, min_z))
        v2 = Vector((max_x, max_y, min_z))
        v3 = Vector((min_x, max_y, min_z))
        v4 = Vector((min_x, min_y, max_z))
        v5 = Vector((max_x, min_y, max_z))
        v6 = Vector((max_x, max_y, max_z))
        v7 = Vector((min_x, max_y, max_z))

        return [
            v0, v1,
            v1, v2,
            v2, v3,
            v3, v0,
            
            v4, v5,
            v5, v6,
            v6, v7,
            v7, v4,
            
            v0, v4,
            v1, v5,
            v2, v6,
            v3, v7 
        ]

    def draw(self, context):
        self.use_draw_scale = False

        self.color = 0.0, 0.0, 1.0
        self.alpha = 1.0
            
        if self.ynd_obj:
            self.custom_shape = self.new_custom_shape(
                "LINES", YndBoundsGizmo.get_verts(self.ynd_obj))
            self.draw_custom_shape(
                self.custom_shape, matrix=self.ynd_obj.matrix_world)


class YndBoundsGizmoGroup(bpy.types.GizmoGroup):
    bl_idname = "OBJECT_GGT_Node_Bounds"
    bl_label = "Node Bounds"
    bl_space_type = "VIEW_3D"
    bl_region_type = "WINDOW"
    bl_options = {"3D", "PERSISTENT"}

    @classmethod
    def poll(cls, context):
        return True

    def setup(self, context):
        pass

    def draw_prepare(self, context):
        self.gizmos.clear()
        for obj in bpy.context.scene.objects:
            if obj.sollum_type == SollumType.NODE_DICTIONARY:
                gz = self.gizmos.new(YndBoundsGizmo.bl_idname)
                gz.ynd_obj = obj