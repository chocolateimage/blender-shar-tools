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

class ShaderTextureParameterChunk(Chunk):
    @staticmethod
    def parseData(data : bytes, isLittleEndian : bool) -> list:
        binaryReader = Pure3DBinaryReader(data, isLittleEndian)

        parameter = binaryReader.readPure3DFourCharacterCode()
        value = binaryReader.readPure3DString()

        return [ parameter, value ]

    def __init__(
        self, 
        identifier: int = chunkIdentifiers.SHADER_TEXTURE_PARAMETER, 
        children : list[Chunk] = None, 
        parameter: str = "", 
        value: str = ""
    ) -> None:
        super().__init__(identifier,children)
    
        self.parameter = parameter
        self.value = value

    def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
        binaryWriter.writePure3DFourCharacterCode(self.parameter)
        binaryWriter.writePure3DString(self.value)