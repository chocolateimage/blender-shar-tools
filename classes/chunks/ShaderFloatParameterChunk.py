from __future__ import annotations

from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

#
# Class
#

class ShaderFloatParameterChunk(Chunk):
    @staticmethod
    def parseData(binaryReader: Pure3DBinaryReader) -> list:
        parameter = binaryReader.readPure3DFourCharacterCode()
        value = binaryReader.readFloat()

        return [ parameter, value ]

    def __init__(
        self, 
        identifier: int = chunkIdentifiers.SHADER_FLOAT_PARAMETER, 
        children : list[Chunk] = None, 
        parameter: str = "", 
        value: float = 0
    ) -> None:
        super().__init__(identifier,children)
    
        self.parameter = parameter
        self.value = value
        
    def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
        binaryWriter.writePure3DFourCharacterCode(self.parameter)
        binaryWriter.writeFloat(self.value)