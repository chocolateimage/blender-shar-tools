from __future__ import annotations

from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

#
# Class
#

class IndexListChunk(Chunk):
    @staticmethod
    def parseData(data : bytes, isLittleEndian : bool) -> list:
        binaryReader = Pure3DBinaryReader(data, isLittleEndian)

        numberOfIndices = binaryReader.readUInt32()
        
        indices = []
        
        for i in range(numberOfIndices):
            indices.append(binaryReader.readUInt32())
        
        return [ indices ]

    def __init__(
        self, 
        identifier: int = chunkIdentifiers.INDEX_LIST, 
        children: list[Chunk] = None, 
        indices: list[int] = None
    ) -> None:
        super().__init__(chunkIdentifiers.INDEX_LIST, children)
    
        self.indices = [] if indices is None else indices

    def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
        binaryWriter.writeUInt32(len(self.indices))

        for index in self.indices:
            binaryWriter.writeUInt32(index)