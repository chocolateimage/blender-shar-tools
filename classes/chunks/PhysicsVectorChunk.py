#
# Imports
#

from __future__ import annotations

from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

import mathutils

#
# Class
#

class PhysicsVectorChunk(Chunk):
    @staticmethod
    def parseData(data : bytes, isLittleEndian : bool) -> list:
        binaryReader = Pure3DBinaryReader(data, isLittleEndian)

        vector = binaryReader.readPure3DVector3()

        return [
            vector
        ]

    def __init__(
        self, 
        identifier: int = chunkIdentifiers.PHYSICS_VECTOR, 
        children : list[Chunk] = None, 
        vector: mathutils.Vector = None
    ) -> None:
        super().__init__(identifier,children)
    
        self.vector = mathutils.Vector() if vector is None else vector

    def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
        binaryWriter.writePure3DVector3(self.vector)