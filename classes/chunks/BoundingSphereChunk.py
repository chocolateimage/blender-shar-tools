from __future__ import annotations

from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

import mathutils

#
# Class
#

class BoundingSphereChunk(Chunk):
    @staticmethod
    def parseData(data : bytes, isLittleEndian : bool) -> list:
        binaryReader = Pure3DBinaryReader(data, isLittleEndian)

        center = binaryReader.readPure3DVector3()
        radius = binaryReader.readFloat()
        
        return [ center, radius ]

    def __init__(
        self, 
        identifier: int = chunkIdentifiers.BOUNDING_SPHERE, 
        children: list[Chunk] = None,
        center: mathutils.Vector = None,
        radius: float = 0
    ) -> None:
        super().__init__(identifier, children)
    
        self.center = mathutils.Vector() if center is None else center
        self.radius = radius

    def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
        binaryWriter.writePure3DVector3(self.center)

        binaryWriter.writeFloat(self.radius)