from __future__ import annotations

from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

#
# Class
#

class CollisionSphereChunk(Chunk):
    @staticmethod
    def parseData(binaryReader: Pure3DBinaryReader) -> list:
        radius = binaryReader.readFloat()

        return [ radius ]

    def __init__(
        self, 
        identifier: int = chunkIdentifiers.COLLISION_SPHERE, 
        children : list[Chunk] = None, 
        radius: float = 0
    ) -> None:
        super().__init__(identifier,children)
    
        self.radius = radius

    def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
        binaryWriter.writeFloat(self.radius)