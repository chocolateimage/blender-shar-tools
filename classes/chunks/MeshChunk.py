from __future__ import annotations

from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

#
# Class
#

class MeshChunk(Chunk):
    @staticmethod
    def parseData(data : bytes, isLittleEndian : bool) -> list:
        binaryReader = Pure3DBinaryReader(data, isLittleEndian)

        name = binaryReader.readPure3DString()
        version = binaryReader.readUInt32()

        return [ name, version ]

    def __init__(
        self, 
        identifier: int = chunkIdentifiers.MESH, 
        children : list[Chunk] = None, 
        name: str = "", 
        version: int = 0
    ) -> None:
        super().__init__(chunkIdentifiers.MESH,children)
    
        self.name = name
        self.version = version
    
    def getNumberOfOldPrimitiveGroups(self) -> int:
        numberOfOldPrimitiveGroups = 0

        for child in self.children:
            if child.identifier == chunkIdentifiers.OLD_PRIMITIVE_GROUP:
                numberOfOldPrimitiveGroups += 1

        return numberOfOldPrimitiveGroups

    def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
        binaryWriter.writePure3DString(self.name)
        binaryWriter.writeUInt32(self.version)
        binaryWriter.writeUInt32(self.getNumberOfOldPrimitiveGroups())