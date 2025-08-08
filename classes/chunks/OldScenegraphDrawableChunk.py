from __future__ import annotations

from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

#
# Class
#

class OldScenegraphDrawableChunk(Chunk):
    @staticmethod
    def parseData(data : bytes, isLittleEndian : bool) -> list:
        binaryReader = Pure3DBinaryReader(data, isLittleEndian)

        name = binaryReader.readPure3DString()

        drawableName = binaryReader.readPure3DString()

        isTranslucent = binaryReader.readUInt32()
        
        return [ name, drawableName, isTranslucent ]

    def __init__(
        self, 
        identifier: int = chunkIdentifiers.OLD_SCENEGRAPH_DRAWABLE, 
        children: list[Chunk] = None,
        name: str = "",
        drawableName: str = "",
        isTranslucent: int = 0,
    ) -> None:
        super().__init__(identifier, children)
    
        self.name = name
        self.drawableName = drawableName
        self.isTranslucent = isTranslucent

    def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
        binaryWriter.writePure3DString(self.name)

        binaryWriter.writePure3DString(self.drawableName)

        binaryWriter.writeUInt32(self.isTranslucent)