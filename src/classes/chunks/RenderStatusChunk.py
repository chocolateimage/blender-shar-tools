#
# Imports
#

from __future__ import annotations

from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

#
# Class
#

class RenderStatusChunk(Chunk):
    @staticmethod
    def parseData(data : bytes, isLittleEndian : bool) -> list:
        binaryReader = Pure3DBinaryReader(data, isLittleEndian)

        castShadow = binaryReader.readUInt32()

        return [
            castShadow,
        ]

    def __init__(
        self, 
        identifier: int = chunkIdentifiers.RENDER_STATUS, 
        children : list[Chunk] = None, 
        castShadow: int = 0,
    ) -> None:
        super().__init__(identifier,children)
    
        self.castShadow = castShadow

    def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
        binaryWriter.writeUInt32(self.castShadow)