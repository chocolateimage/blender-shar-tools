from __future__ import annotations

from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

#
# Class
#

class VertexShaderChunk(Chunk):
    @staticmethod
    def parseData(data : bytes, isLittleEndian : bool) -> list:
        binaryReader = Pure3DBinaryReader(data, isLittleEndian)

        vertexShaderName = binaryReader.readPure3DString()
        
        return [ vertexShaderName ]

    def __init__(
        self, 
        identifier: int = chunkIdentifiers.VERTEX_SHADER, 
        children: list[Chunk] = None,
        vertexShaderName: str = ""
    ) -> None:
        super().__init__(identifier, children)
    
        self.vertexShaderName = vertexShaderName

    def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
        binaryWriter.writePure3DString(self.vertexShaderName)