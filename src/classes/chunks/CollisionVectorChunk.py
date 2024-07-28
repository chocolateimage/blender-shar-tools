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

class CollisionVectorChunk(Chunk):
	@staticmethod
	def parseData(data : bytes, isLittleEndian : bool) -> list:
		binaryReader = Pure3DBinaryReader(data, isLittleEndian)

		vector = binaryReader.readPure3DVector3()

		return [ vector ]

	def __init__(
		self, 
		identifier: int = chunkIdentifiers.COLLISION_VECTOR, 
		children : list[Chunk] = [], 
		vector: mathutils.Vector = mathutils.Vector()
	) -> None:
		super().__init__(identifier,children)
	
		self.vector = vector

	def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
		binaryWriter.writePure3DVector3(self.vector)