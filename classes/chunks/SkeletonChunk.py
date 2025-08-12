from __future__ import annotations

from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

class SkeletonChunk(Chunk):
    @staticmethod
    def parseData(binaryReader: Pure3DBinaryReader) -> list:
        name = binaryReader.readPure3DString()
        version = binaryReader.readUInt32()
        
        return [name, version]

    def __init__(
        self, 
        identifier: int = chunkIdentifiers.SKELETON, 
        children: list[Chunk] = None,
        name: str = "",
        version: int = 0,
    ) -> None:
        super().__init__(identifier, children)
    
        self.name = name
        self.version = version

    def getNumberOfJoints(self):
        amount = 0
        for i in self.children:
            if i.identifier == chunkIdentifiers.SKELETON_JOINT:
                amount += 1
        return amount

    def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
        binaryWriter.writePure3DString(self.name)
        binaryWriter.writeUInt32(self.version)

        binaryWriter.writeUInt32(self.getNumberOfJoints())
