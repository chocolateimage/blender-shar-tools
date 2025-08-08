from __future__ import annotations

from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

import mathutils

#
# Class
#

class IntersectChunk(Chunk):
    @staticmethod
    def parseData(data : bytes, isLittleEndian : bool) -> list:
        binaryReader = Pure3DBinaryReader(data, isLittleEndian)

        indexCount = binaryReader.readUInt32()
        indices = []
        for i in range(indexCount):
            indices.append(binaryReader.readUInt32())
        positionCount = binaryReader.readUInt32()
        positions = []
        for i in range(positionCount):
            positions.append(binaryReader.readPure3DVector3())
        normalCount = binaryReader.readUInt32()
        normals = []
        for i in range(normalCount):
            normals.append(binaryReader.readPure3DVector3())

        return [ indices, positions, normals ]

    def __init__(
        self, 
        identifier: int = chunkIdentifiers.INTERSECT, 
        children : list[Chunk] = None, 
        indices: list[int] = None,
        positions: list[mathutils.Vector] = None,
        normals: list[mathutils.Vector] = None,
    ) -> None:
        super().__init__(identifier,children)
    
        self.indices = indices
        self.positions = positions
        self.normals = normals
    
    def getNumberOfOldPrimitiveGroups(self) -> int:
        numberOfOldPrimitiveGroups = 0

        for child in self.children:
            if child.identifier == chunkIdentifiers.OLD_PRIMITIVE_GROUP:
                numberOfOldPrimitiveGroups += 1

        return numberOfOldPrimitiveGroups

    def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
        binaryWriter.writeUInt32(len(self.indices))
        for i in self.indices:
            binaryWriter.writeUInt32(i)
        binaryWriter.writeUInt32(len(self.positions))
        for i in self.positions:
            binaryWriter.writePure3DVector3(i)
        binaryWriter.writeUInt32(len(self.normals))
        for i in self.normals:
            binaryWriter.writePure3DVector3(i)