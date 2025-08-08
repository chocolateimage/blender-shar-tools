from __future__ import annotations

from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

#
# Class
#

class OldScenegraphBranchChunk(Chunk):
    @staticmethod
    def parseData(data : bytes, isLittleEndian : bool) -> list:
        binaryReader = Pure3DBinaryReader(data, isLittleEndian)

        name = binaryReader.readPure3DString()
        
        return [ name ]

    def __init__(
        self, 
        identifier: int = chunkIdentifiers.OLD_SCENEGRAPH_BRANCH, 
        children: list[Chunk] = None,
        name: str = "",
    ) -> None:
        super().__init__(identifier, children)
    
        self.name = name

    def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
        binaryWriter.writePure3DString(self.name)

        binaryWriter.writeUInt32(len(self.children))