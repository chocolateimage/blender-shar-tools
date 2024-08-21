#
# Imports
#

from __future__ import annotations

from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

import mathutils

#
# Class
#

class OldScenegraphTransformChunk(Chunk):
	@staticmethod
	def parseData(data : bytes, isLittleEndian : bool) -> list:
		binaryReader = Pure3DBinaryReader(data, isLittleEndian)

		name = binaryReader.readPure3DString()
		numberOfChildren = binaryReader.readUInt32()
		matrix = binaryReader.readPure3DMatrix()
		
		return [ name, matrix ]

	def __init__(
		self, 
		identifier: int = chunkIdentifiers.OLD_SCENEGRAPH_TRANSFORM, 
		children: list[Chunk] = None,
		name: str = "",
		matrix: mathutils.Matrix = None,
	) -> None:
		super().__init__(identifier, children)
	
		self.name = name
		self.matrix = mathutils.Matrix() if matrix is None else matrix

	def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
		binaryWriter.writePure3DString(self.name)

		binaryWriter.writeUInt32(len(self.children))

		binaryWriter.writePure3DMatrix(self.matrix)