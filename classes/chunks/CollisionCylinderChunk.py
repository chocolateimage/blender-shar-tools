#
# Imports
#

from __future__ import annotations

from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

#
# Class
#

class CollisionCylinderChunk(Chunk):
    @staticmethod
    def parseData(data : bytes, isLittleEndian : bool) -> list:
        binaryReader = Pure3DBinaryReader(data, isLittleEndian)

        cylinderRadius = binaryReader.readFloat()
        length = binaryReader.readFloat()
        flatEnd = binaryReader.readUInt16()

        return [ cylinderRadius, length, flatEnd ]

    def __init__(
        self, 
        identifier: int = chunkIdentifiers.COLLISION_CYLINDER, 
        children : list[Chunk] = None, 
        cylinderRadius: float = 0,
        length: int = 0,
        flatEnd: int = 0
    ) -> None:
        super().__init__(identifier,children)
    
        self.cylinderRadius = cylinderRadius
        self.length = length
        self.flatEnd = flatEnd

    def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
        binaryWriter.writeFloat(self.cylinderRadius)

        binaryWriter.writeFloat(self.length)

        binaryWriter.writeUInt16(self.flatEnd)