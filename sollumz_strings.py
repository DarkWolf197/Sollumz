import traceback
import os
from typing import Optional
import bpy
from bpy_extras.io_utils import ImportHelper
from .sollumz_helper import SOLLUMZ_OT_base, find_sollumz_parent
from .sollumz_preferences import get_addon_preferences, _save_preferences
from .sollumz_operators import TimedOperator
from .tools.jenkhash import name_to_hash
from . import logger


class SOLLUMZ_OT_import_strings(bpy.types.Operator, ImportHelper, TimedOperator):
    """Import Strings from a .txt or .nametable file"""
    bl_idname = "sollumz.import_strings"
    bl_label = "Import Strings"
    bl_options = {"UNDO"}

    directory: bpy.props.StringProperty(subtype="FILE_PATH", options={"HIDDEN", "SKIP_SAVE"})
    files: bpy.props.CollectionProperty(
        name="File Path",
        type=bpy.types.OperatorFileListElement,
        options={"HIDDEN", "SKIP_SAVE"}
    )

    filter_glob: bpy.props.StringProperty(
        default="".join(f"*{filetype};" for filetype in (".txt")),
        options={"HIDDEN", "SKIP_SAVE"},
        maxlen=255,
    )

    def draw(self, context):
        pass

    def execute_timed(self, context):
        with logger.use_operator_logger(self):
            if not self.directory or len(self.files) == 0 or self.files[0].name == "":
                logger.info("No file selected for import!")
                return {"CANCELLED"}
            
            self.directory = bpy.path.abspath(self.directory)
            prefs = get_addon_preferences(context)

            filenames = [f.name for f in self.files]

            for filename in filenames:
                filepath = os.path.join(self.directory, filename)

                try:
                    with open(filepath, "r") as open_file:
                        for line in open_file:
                            line = line.strip()
                            if line:
                                new_string = prefs.loaded_strings.add()
                                new_string.string = line
                                new_string.hash = f"hash_{name_to_hash(line)}"

                    _save_preferences()

                    logger.info(f"Successfully imported '{filepath}'")
                except:
                    logger.error(f"Error importing: {filepath} \n {traceback.format_exc()}")
                    return {"CANCELLED"}

            logger.info(f"Imported in {self.time_elapsed} seconds")
            return {"FINISHED"}



class SOLLUMZ_OT_remove_strings(SOLLUMZ_OT_base, bpy.types.Operator):
    """Remove all loaded strings"""
    bl_idname = "sollumz.remove_strings"
    bl_label = "Remove Strings"

    @classmethod
    def poll(cls, context):
        prefs = get_addon_preferences(context)
        return len(prefs.loaded_strings) > 0

    def run(self, context):
        prefs = get_addon_preferences(context)
        prefs.loaded_strings.clear()
        _save_preferences()
        return {"FINISHED"}


class SOLLUMZ_OT_save_strings(SOLLUMZ_OT_base, bpy.types.Operator):
    """Esporta tutte le stringhe in un file .txt"""
    bl_idname = "sollumz.save_strings"
    bl_label = "Esporta Stringhe"
    bl_options = {'REGISTER', 'UNDO'}
    
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    
    @classmethod
    def poll(cls, context):
        prefs = get_addon_preferences(context)
        return len(prefs.loaded_strings) > 0

    def execute_timed(self, context):
        prefs = get_addon_preferences(context)
        with logger.use_operator_logger(self):
            if not prefs.loaded_strings or len(prefs.loaded_strings) <= 0:
                logger.info("No strings to export!")
                return {"CANCELLED"}
            
            self.directory = bpy.path.abspath(self.directory)

            filenames = [f.name for f in self.files]

            for filename in filenames:
                filepath = os.path.join(self.directory, filename)

                try:
                    with open(self.filepath, 'w', encoding='utf-8') as file:
                        for item in prefs.loaded_strings:
                            file.write(f"{item.string}\n")

                    logger.info(f"Successfully exported '{filepath}'")
                except:
                    logger.error(f"Error exporting: {filepath} \n {traceback.format_exc()}")
                    return {"CANCELLED"}

            logger.info(f"Exported in {self.time_elapsed} seconds")
            return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}