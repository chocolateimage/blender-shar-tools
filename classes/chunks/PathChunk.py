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

class PathChunk(Chunk):
    @staticmethod
    def parseData(data : bytes, isLittleEndian : bool) -> list:
        binaryReader = Pure3DBinaryReader(data, isLittleEndian)

        numberOfPoints = binaryReader.readUInt32()

        points = []

        for i in range(numberOfPoints):
            points.append(binaryReader.readPure3DVector3())

        return [ points ]

    def __init__(
        self, 
        identifier : int = chunkIdentifiers.PATH, 
        children : list[Chunk] = None, 
        points : list[mathutils.Vector] = None
    ) -> None:
        super().__init__(chunkIdentifiers.PATH, children)

        self.points = [] if points is None else points
        
    def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
        binaryWriter.writeUInt32(len(self.points))

        for point in self.points:
            binaryWriter.writePure3DVector3(point)