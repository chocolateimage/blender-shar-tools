from __future__ import annotations

from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

#
# Class
#

class ImageChunk(Chunk):
    # TODO: Either move to a sub class or a "data" file like the Chunk Identifiers
    formats = {
        "RAW": 0,
        "PNG": 1,
        "TGA": 2,
        "BMP": 3,
        "IPU": 4,
        "DXT": 5,
        "DXT1": 6,
        "DXT2": 7,
        "DXT3": 8,
        "DXT4": 9,
        "DXT5": 10,
        "PS24BIT": 11,
        "PS28BIT": 12,
        "PS216BIT": 13,
        "PS232BIT": 14,
        "GC4BIT": 15,
        "GC8BIT": 16,
        "GC16BIT": 17,
        "GC32BIT": 18,
        "GCDXT1": 19,
        "OTHER": 20,
        "INVALID": 21,
        "PSP4BIT": 22,
    }
    
    @staticmethod
    def parseData(data : bytes, isLittleEndian : bool) -> list:
        binaryReader = Pure3DBinaryReader(data, isLittleEndian)

        name = binaryReader.readPure3DString()
        version = binaryReader.readUInt32()
        width = binaryReader.readUInt32()
        height = binaryReader.readUInt32()
        bitsPerPixel = binaryReader.readUInt32()
        palettized = binaryReader.readUInt32()
        hasAlpha = binaryReader.readUInt32()
        format = binaryReader.readUInt32()

        return [ name, version, width, height, bitsPerPixel, palettized, hasAlpha, format ]

    def __init__(
        self, 
        identifier: int = chunkIdentifiers.IMAGE, 
        children: list[Chunk] = None, 
        name: str = "", 
        version: int = 0, 
        width: int = 0, 
        height: int = 0, 
        bitsPerPixel: int = 0, 
        palettized: int = 0, 
        hasAlpha: int = 0, 
        format: int = 0
    ) -> None:
        super().__init__(chunkIdentifiers.IMAGE, children)
    
        self.name = name
        self.version = version
        self.width = width
        self.height = height
        self.bitsPerPixel = bitsPerPixel
        self.palettized = palettized
        self.hasAlpha = hasAlpha
        self.format = format

    def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
        binaryWriter.writePure3DString(self.name)
        binaryWriter.writeUInt32(self.version)
        binaryWriter.writeUInt32(self.width)
        binaryWriter.writeUInt32(self.height)
        binaryWriter.writeUInt32(self.bitsPerPixel)
        binaryWriter.writeUInt32(self.palettized)
        binaryWriter.writeUInt32(self.hasAlpha)
        binaryWriter.writeUInt32(self.format)