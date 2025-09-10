from abc import ABC as AbstractClass
from .element import (
    ElementTree,
    ValueProperty,
    ListPropertyRequired,
)


class WATER:

    file_extension = ["water.xml", "water_heistisland.xml"]

    @staticmethod
    def from_xml_file(filepath):
        return WaterData.from_xml_file(filepath)

    @staticmethod
    def write_xml(water_data, filepath):
        return water_data.write_xml(filepath)


class WaterQuad(ElementTree):
    tag_name = "Item"

    def __init__(self):
        super().__init__()
        self.min_x = ValueProperty("minX")
        self.max_x = ValueProperty("maxX")
        self.min_y = ValueProperty("minY")
        self.max_y = ValueProperty("maxY")
        self.type = ValueProperty("Type")
        self.is_invisible = ValueProperty("IsInvisible")
        self.has_limited_depth = ValueProperty("HasLimitedDepth")
        self.z = ValueProperty("z")
        self.a1 = ValueProperty("a1")
        self.a2 = ValueProperty("a2")
        self.a3 = ValueProperty("a3")
        self.a4 = ValueProperty("a4")
        self.no_stencil = ValueProperty("NoStencil")


class CalmingQuad(ElementTree):
    tag_name = "Item"

    def __init__(self):
        super().__init__()
        self.min_x = ValueProperty("minX")
        self.max_x = ValueProperty("maxX")
        self.min_y = ValueProperty("minY")
        self.max_y = ValueProperty("maxY")
        self.f_dampening = ValueProperty("fDampening")


class WaveQuad(ElementTree):
    tag_name = "Item"

    def __init__(self):
        super().__init__()
        self.min_x = ValueProperty("minX")
        self.max_x = ValueProperty("maxX")
        self.min_y = ValueProperty("minY")
        self.max_y = ValueProperty("maxY")
        self.amplitude = ValueProperty("Amplitude")
        self.x_direction = ValueProperty("XDirection")
        self.y_direction = ValueProperty("YDirection")


class WaterList(ListPropertyRequired):
    list_type = WaterQuad
    tag_name = "WaterQuads"


class CalmingList(ListPropertyRequired):
    list_type = CalmingQuad
    tag_name = "CalmingQuads"


class WaveList(ListPropertyRequired):
    list_type = WaveQuad
    tag_name = "WaveQuads"


class WaterData(ElementTree, AbstractClass):
    tag_name = "WaterData"

    def __init__(self):
        super().__init__()
        self.water_quads = WaterList()
        self.calming_quads = CalmingList()
        self.wave_quads = WaveList()
