import bpy
from ..cwxml.ynd import *


def ynd_from_object(obj):
    ynd = NodeDictionary()

    return ynd

def export_ynd(obj: bpy.types.Object, filepath: str) -> bool:
    ynd = ynd_from_object(obj)
    ynd.write_xml(filepath)
    return True
