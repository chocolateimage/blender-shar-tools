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

class InstStatEntityChunk(Chunk):
    @staticmethod
    def parseData(data : bytes, isLittleEndian : bool) -> list:
        binaryReader = Pure3DBinaryReader(data, isLittleEndian)

        name = binaryReader.readPure3DString()
        version = binaryReader.readUInt32()
        hasAlpha = binaryReader.readUInt32()
        
        return [ name, version, hasAlpha ]

    def __init__(
        self, 
        identifier: int = chunkIdentifiers.INST_STAT_ENTITY, 
        children: list[Chunk] = None,
        name: str = "",
        version: int = 0,
        hasAlpha: int = 0
    ) -> None:
        super().__init__(identifier, children)
    
        self.name = name
        self.version = version
        self.hasAlpha = hasAlpha

    def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
        binaryWriter.writePure3DString(self.name)

        binaryWriter.writeUInt32(self.version)
        binaryWriter.writeUInt32(self.hasAlpha)