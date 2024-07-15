#
# Imports
#

from __future__ import annotations

import typing

from classes.chunks.Chunk import Chunk

import classes.Pure3DBinaryReader
import classes.Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

#
# Class
#

class ShaderTextureParameterChunk(classes.chunks.Chunk.Chunk):
	@staticmethod
	def parseData(data : bytes, isLittleEndian : bool) -> list:
		binaryReader = classes.Pure3DBinaryReader.Pure3DBinaryReader(data, isLittleEndian)

		parameter = binaryReader.readPure3DFourCharacterCode()
		value = binaryReader.readPure3DString()

		return [parameter,value]

	def __init__(self, identifier: chunkIdentifiers.SHADER_TEXTURE_PARAMETER, children : list[Chunk] | None = None, parameter: str = "", value: str = "") -> None:
		super().__init__(identifier,children)
	
		self.parameter = parameter
		self.value = value
		

	def writeData(self, binaryWriter : classes.Pure3DBinaryWriter.Pure3DBinaryWriter) -> None:
		binaryWriter.writePure3DFourCharacterCode(self.parameter)
		binaryWriter.writePure3DString(self.value)