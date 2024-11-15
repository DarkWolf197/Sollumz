import bpy
from bpy.props import StringProperty

class WIP_OT_CreateLink(bpy.types.Operator):
    bl_idname = "sollumz.createlink"
    bl_label = "Create Link"
    bl_options = {'REGISTER', 'UNDO'}

    link_name: StringProperty(name="Link Name", default="New Link")

    def execute(self, context):
        # Aggiungi la logica per creare un link qui
        self.report({'INFO'}, f"Link '{self.link_name}' creato")
        return {'FINISHED'}

class WIP_OT_DeleteLink(bpy.types.Operator):
    bl_idname = "sollumz.deletelink"
    bl_label = "Delete Link"
    bl_options = {'REGISTER', 'UNDO'}

    link_name: StringProperty(name="Link Name", default="Link to delete")

    def execute(self, context):
        # Aggiungi la logica per eliminare un link qui
        self.report({'INFO'}, f"Link '{self.link_name}' eliminato")
        return {'FINISHED'}