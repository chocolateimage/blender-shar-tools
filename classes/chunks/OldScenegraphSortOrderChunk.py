from __future__ import annotations

from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

#
# Class
#

class OldScenegraphSortOrderChunk(Chunk):
    @staticmethod
    def parseData(binaryReader: Pure3DBinaryReader) -> list:
        sortOrder = binaryReader.readFloat()
        
        return [ sortOrder ]

    def __init__(
        self, 
        identifier: int = chunkIdentifiers.OLD_SCENEGRAPH_SORT_ORDER, 
        children: list[Chunk] = None,
        sortOrder: float = 0,
    ) -> None:
        super().__init__(identifier, children)
    
        self.sortOrder = sortOrder

    def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
        binaryWriter.writeFloat(self.sortOrder)