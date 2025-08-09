from __future__ import annotations

from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

import mathutils

#
# Class
#

class UVListChunk(Chunk):
    @staticmethod
    def parseData(binaryReader: Pure3DBinaryReader) -> list:
        numberOfUVs = binaryReader.readUInt32()
        channel = binaryReader.readUInt32()
        
        uvs = []
        
        for i in range(numberOfUVs):
            uvs.append(binaryReader.readPure3DVector2())

        return [ channel, uvs ]

    def __init__(
        self, 
        identifier: int = chunkIdentifiers.UV_LIST, 
        children : list[Chunk] = None, 
        channel: int = 0, 
        uvs: list[mathutils.Vector] = None
    ) -> None:
        super().__init__(identifier,children)
    
        self.channel = channel
        self.uvs = [] if uvs is None else uvs

    def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
        binaryWriter.writeUInt32(len(self.uvs))
        binaryWriter.writeUInt32(self.channel)

        for uv in self.uvs:
            binaryWriter.writePure3DVector2(uv)
