from __future__ import annotations

from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

#
# Class
#

class CollisionAxisAlignedBoundingBoxChunk(Chunk):
    @staticmethod
    def parseData(data : bytes, isLittleEndian : bool) -> list:
        binaryReader = Pure3DBinaryReader(data, isLittleEndian)

        nothing = binaryReader.readUInt32()

        return [
            nothing,
        ]

    def __init__(
        self, 
        identifier: int = chunkIdentifiers.COLLISION_AXIS_ALIGNED_BOUNDING_BOX, 
        children : list[Chunk] = None, 
        nothing: int = 0,
    ) -> None:
        super().__init__(identifier,children)
    
        self.nothing = nothing

    def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
        binaryWriter.writeUInt32(self.nothing)