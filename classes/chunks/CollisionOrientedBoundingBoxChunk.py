from __future__ import annotations

from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

import mathutils

#
# Class
#

class CollisionOrientedBoundingBoxChunk(Chunk):
    @staticmethod
    def parseData(binaryReader: Pure3DBinaryReader) -> list:
        halfExtents = binaryReader.readPure3DVector3()

        return [ halfExtents ]

    def __init__(
        self, 
        identifier: int = chunkIdentifiers.COLLISION_ORIENTED_BOUNDING_BOX, 
        children : list[Chunk] = None, 
        halfExtents: mathutils.Vector = None
    ) -> None:
        super().__init__(identifier,children)
    
        self.halfExtents = mathutils.Vector() if halfExtents is None else halfExtents

    def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
        binaryWriter.writePure3DVector3(self.halfExtents)