from __future__ import annotations

from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

#
# Class
#

class SurfaceTypeListChunk(Chunk):
    @staticmethod
    def parseData(data : bytes, isLittleEndian : bool) -> list:
        binaryReader = Pure3DBinaryReader(data, isLittleEndian)

        version = binaryReader.readUInt32()

        typeCount = binaryReader.readUInt32()
        types = []
        for i in range(typeCount):
            types.append(binaryReader.readByte())
        
        return [ version, types ]

    def __init__(
        self, 
        identifier: int = chunkIdentifiers.SURFACE_TYPE_LIST, 
        children: list[Chunk] = None,
        version: int = 0,
        types: list[int] = None
    ) -> None:
        super().__init__(identifier, children)
    
        self.version = version
        self.types = [] if types is None else types

    def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
        binaryWriter.writeUInt32(self.version)

        binaryWriter.writeUInt32(len(self.types))

        for i in self.types:
            binaryWriter.writeByte(i)
