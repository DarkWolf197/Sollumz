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

        # Verifica che l'oggetto abbia le proprietà necessarie
        if not hasattr(obj, "node_properties") or not hasattr(obj.node_properties, "links"):
            self.report({'ERROR'}, "Oggetto non ha proprietà di link.")
            return {'CANCELLED'}

        # Verifica se l'indice è valido
        link_index = obj.node_properties.link_index
        links = obj.node_properties.links

        if link_index < 0 or link_index >= len(links):
            self.report({'ERROR'}, "Indice di link non valido.")
            return {'CANCELLED'}

        # Recupera il link selezionato
        selected_link = links[link_index]

        # Verifica se esiste un oggetto collegato
        linked_obj = getattr(selected_link, "linked_obj", None)

        # Rimuovi il link dall'oggetto corrente
        links.remove(link_index)

        # Rimuovi il link dall'oggetto collegato, se esiste
        if linked_obj and hasattr(linked_obj, "node_properties") and hasattr(linked_obj.node_properties, "links"):
            for i, link in enumerate(linked_obj.node_properties.links):
                if link.linked_obj == obj:
                    linked_obj.node_properties.links.remove(i)
                    break

        # Report informativo
        if linked_obj:
            self.report({'INFO'}, f"Link rimosso tra {obj.name} e {linked_obj.name}.")
        else:
            self.report({'INFO'}, f"Link rimosso dall'oggetto {obj.name}.")

        return {'FINISHED'}