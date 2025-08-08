from __future__ import annotations

from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

import mathutils

#
# Class
#

class BoundingBoxChunk(Chunk):
    @staticmethod
    def parseData(data : bytes, isLittleEndian : bool) -> list:
        binaryReader = Pure3DBinaryReader(data, isLittleEndian)

        low = binaryReader.readPure3DVector3()
        high = binaryReader.readPure3DVector3()
        
        return [ low, high ]

    def __init__(
        self, 
        identifier: int = chunkIdentifiers.BOUNDING_BOX, 
        children: list[Chunk] = None,
        low: mathutils.Vector = None,
        high: mathutils.Vector = None,
    ) -> None:
        super().__init__(identifier, children)
    
        self.low = mathutils.Vector() if low is None else low
        self.high = mathutils.Vector() if high is None else high

    def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
        binaryWriter.writePure3DVector3(self.low)

        binaryWriter.writePure3DVector3(self.high)