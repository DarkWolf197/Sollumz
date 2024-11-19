import bpy
from bpy.props import StringProperty
from ..sollumz_helper import SOLLUMZ_OT_base
from ..sollumz_properties import SollumType, SOLLUMZ_UI_NAMES
from .utils import find_node
from ..tools.yndhelper import create_nodedict, create_node


class SOLLUMZ_OT_create_nodedict(SOLLUMZ_OT_base, bpy.types.Operator):
    """Create a sollumz YND object"""
    bl_idname = "sollumz.createnodedict"
    bl_label = f"Create NodeDict"
    bl_description = "Create a NodeDict"

    def run(self, context):
        nodedict_obj = create_nodedict()
        if nodedict_obj:
            bpy.ops.object.select_all(action='DESELECT')
            nodedict_obj.select_set(True)
            context.view_layer.objects.active = nodedict_obj
        return {"FINISHED"}


class SOLLUMZ_OT_create_node(SOLLUMZ_OT_base, bpy.types.Operator):
    """Create a sollumz YND object"""
    bl_idname = "sollumz.createnode"
    bl_label = f"Create Node"
    bl_description = "Create a Node"
        
    def run(self, context):
        node_obj = create_node(parent_obj=context.active_object)
        if node_obj:
            bpy.ops.object.select_all(action='DESELECT')
            node_obj.select_set(True)
            context.view_layer.objects.active = node_obj
        return {"FINISHED"}


class SOLLUMZ_OT_create_link(bpy.types.Operator):
    """Create a sollumz link between two objects"""
    bl_idname = "sollumz.createlink"
    bl_label = "Create Link"

    def execute(self, context):
        selected_objects = context.selected_objects
        if len(selected_objects) == 2:
            self.report({'INFO'}, "Created Link")
            obj1, obj2 = selected_objects  # Estraggo i due oggetti
            # Creare i link con il nome dell'altro oggetto
            link_obj1 = obj1.node_properties.links.add()
            link_obj1.name = obj2.name
            link_obj2 = obj2.node_properties.links.add()
            link_obj2.name = obj1.name
            return {'FINISHED'}
        else:
            self.report({'INFO'}, "Needs two objects selected")
            return {'FINISHED'}



class WIP_OT_DeleteLink(bpy.types.Operator):
    bl_idname = "sollumz.deletelink"
    bl_label = "Delete Link"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        self.report({'INFO'}, f"WIP")
        return {'FINISHED'}