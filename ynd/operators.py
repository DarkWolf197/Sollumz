import bpy
from bpy.props import StringProperty
from ..sollumz_helper import SOLLUMZ_OT_base
from ..sollumz_properties import SollumType, SOLLUMZ_UI_NAMES
from .utils import find_node
from ..tools.yndhelper import create_nodedict, create_node


class SOLLUMZ_OT_goto_node(bpy.types.Operator):
    """Teleport to a linked node"""
    bl_idname = "sollumz.gotonode"
    bl_label = "Go to Linked Node"
    bl_description = "Navigate to the object linked to the current node"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        if not context.active_object:
            return False
        
        node_props = getattr(context.active_object, 'node_properties', None)
        if not node_props:
            return False
        
        link_index = getattr(node_props, 'link_index', -1)
        links = getattr(node_props, 'links', [])
        
        return (0 <= link_index < len(links) and 
                getattr(links[link_index], 'linked_obj', None) is not None)

    def execute(self, context):
        obj = context.active_object
        node_props = obj.node_properties
        
        linked_obj = node_props.links[node_props.link_index].linked_obj
        
        bpy.ops.object.select_all(action='DESELECT')
        linked_obj.select_set(True)
        context.view_layer.objects.active = linked_obj
        
        bpy.ops.view3d.view_selected(use_all_regions=True)

        return {'FINISHED'}



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
    """Create a sollumz link between multiple objects"""
    bl_idname = "sollumz.createlink"
    bl_label = "Create Link"

    def execute(self, context):
        selected_objects = context.selected_objects
        
        if len(selected_objects) < 2:
            self.report({'INFO'}, "Needs at least two objects selected")
            return {'CANCELLED'}

        selected_objects = sorted(selected_objects, key=lambda obj: obj.node_properties.node_id)

        for i in range(len(selected_objects) - 1):
            obj1 = selected_objects[i]
            obj2 = selected_objects[i + 1]
            
            link_obj1 = obj1.node_properties.links.add()
            link_obj1.name = obj2.name
            link_obj1.to_node_id = obj2.node_properties.node_id
            link_obj1.to_area_id = obj2.node_properties.area_id
            link_obj1.linked_obj = obj2

            link_obj2 = obj2.node_properties.links.add()
            link_obj2.name = obj1.name
            link_obj2.to_node_id = obj1.node_properties.node_id
            link_obj2.to_area_id = obj1.node_properties.area_id
            link_obj2.linked_obj = obj1

        self.report({'INFO'}, f"Created {len(selected_objects) - 1} links")
        return {'FINISHED'}


class SOLLUMZ_OT_fix_node_ids(bpy.types.Operator):
    bl_idname = "sollumz.fixnodeids"
    bl_label = "Fix Node ID's"

    def execute(self, context):
        selected_dict = context.active_object

        for i, child in enumerate(selected_dict.children):
            child.node_properties.node_id = i

        return {'FINISHED'}


class SOLLUMZ_OT_delete_link(bpy.types.Operator):
    bl_idname = "sollumz.deletelink"
    bl_label = "Delete Link"

    def execute(self, context):
        obj = context.active_object

        links = obj.node_properties.links
        link_index = obj.node_properties.link_index
        selected_link = links[link_index]

        linked_obj = selected_link.linked_obj

        if linked_obj and hasattr(linked_obj, "node_properties") and hasattr(linked_obj.node_properties, "links"):
            for i, link in enumerate(linked_obj.node_properties.links):
                if link.linked_obj == obj:
                    linked_obj.node_properties.links.remove(i)
                    break
        
        links.remove(link_index)

        if len(links) > 0:
            obj.node_properties.link_index = min(link_index, len(links) - 1)
        else:
            obj.node_properties.link_index = -1

        return {'FINISHED'}