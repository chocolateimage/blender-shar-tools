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

class PhysicsInertiaMatrixChunk(Chunk):
	@staticmethod
	def parseData(data : bytes, isLittleEndian : bool) -> list:
		binaryReader = Pure3DBinaryReader(data, isLittleEndian)

		x = binaryReader.readPure3DVector3()
		yy = binaryReader.readFloat()
		yz = binaryReader.readFloat()
		zz = binaryReader.readFloat()

		return [
			x,
			yy,
			yz,
			zz
		]

	def __init__(
		self, 
		identifier: int = chunkIdentifiers.PHYSICS_INERTIA_MATRIX, 
		children : list[Chunk] = None, 
		x: mathutils.Vector = None,
		yy: float = 0,
		yz: float = 0,
		zz: float = 0
	) -> None:
		super().__init__(identifier,children)
	
		self.x = mathutils.Vector() if x is None else x
		self.yy = yy
		self.yz = yz
		self.zz = zz

	def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
		binaryWriter.writePure3DVector3(self.x)
		binaryWriter.writeFloat(self.yy)
		binaryWriter.writeFloat(self.yz)
		binaryWriter.writeFloat(self.zz)