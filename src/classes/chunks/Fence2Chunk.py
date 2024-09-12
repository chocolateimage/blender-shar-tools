#
# Imports
#

from __future__ import annotations

import mathutils

from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

#
# Class
#

class Fence2Chunk(Chunk):
    @staticmethod
    def parseData(data : bytes, isLittleEndian : bool) -> list:
        binaryReader = Pure3DBinaryReader(data, isLittleEndian)

        start = binaryReader.readPure3DVector3()
        end = binaryReader.readPure3DVector3()
        normal = binaryReader.readPure3DVector3()

        return [ start, end, normal ]

    def __init__(
        self, 
        identifier : int = chunkIdentifiers.FENCE_2, 
        children : list[Chunk] = None, 
        start : mathutils.Vector = None, 
        end : mathutils.Vector = None, 
        normal : mathutils.Vector = None
    ) -> None:
        super().__init__(chunkIdentifiers.FENCE_2, children)

        self.start : mathutils.Vector = mathutils.Vector((0, 0, 0)) if start is None else start
        self.end : mathutils.Vector = mathutils.Vector((0, 0, 0)) if end is None else end
        self.normal : mathutils.Vector = mathutils.Vector((0, 0, 0)) if normal is None else normal

    def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
        binaryWriter.writePure3DVector3(self.start)
        binaryWriter.writePure3DVector3(self.end)
        binaryWriter.writePure3DVector3(self.normal)