#
# Imports
#

from __future__ import annotations

from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

from classes.Colour import Colour

import data.chunkIdentifiers as chunkIdentifiers

import mathutils

#
# Classes
#

class GameAttrChunk(Chunk):
	@staticmethod
	def parseData(data : bytes, isLittleEndian : bool) -> list:
		binaryReader = Pure3DBinaryReader(data, isLittleEndian)

		name = binaryReader.readPure3DString()
		version = binaryReader.readUInt32()
		binaryReader.readUInt32() # Number of parameters

		return [ name, version ]

	def __init__(
		self, 
		identifier: int = chunkIdentifiers.GAME_ATTR, 
		children : list[Chunk] = None, 
		name: str = "", 
		version: int = 0
	) -> None:
		super().__init__(identifier,children)
	
		self.name = name
		self.version = version
		
	def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
		binaryWriter.writePure3DString(self.name)
		binaryWriter.writeUInt32(self.version)
		binaryWriter.writeUInt32(len(self.children))

class GameAttrIntegerParameterChunk(Chunk):
	@staticmethod
	def parseData(data : bytes, isLittleEndian : bool) -> list:
		binaryReader = Pure3DBinaryReader(data, isLittleEndian)

		parameter = binaryReader.readPure3DString()
		value = binaryReader.readUInt32()

		return [ parameter, value ]

	def __init__(
		self, 
		identifier: int = chunkIdentifiers.GAME_ATTRIBUTE_INTEGER_PARAMETER, 
		children : list[Chunk] = None, 
		parameter: str = "", 
		value: int = 0
	) -> None:
		super().__init__(identifier,children)
	
		self.parameter = parameter
		self.value = value
		
	def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
		binaryWriter.writePure3DString(self.parameter)
		binaryWriter.writeUInt32(self.value)

class GameAttrColourParameterChunk(Chunk):
	@staticmethod
	def parseData(data : bytes, isLittleEndian : bool) -> list:
		binaryReader = Pure3DBinaryReader(data, isLittleEndian)

		parameter = binaryReader.readPure3DString()
		value = binaryReader.readPure3DColour()

		return [ parameter, value ]

	def __init__(
		self, 
		identifier: int = chunkIdentifiers.GAME_ATTRIBUTE_COLOUR_PARAMETER, 
		children : list[Chunk] = None, 
		parameter: str = "", 
		value: Colour = None
	) -> None:
		super().__init__(identifier,children)
	
		self.parameter = parameter
		self.value = Colour() if value is None else value
		
	def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
		binaryWriter.writePure3DString(self.parameter)
		binaryWriter.writePure3DColour(self.value)

class GameAttrMatrixParameterChunk(Chunk):
	@staticmethod
	def parseData(data : bytes, isLittleEndian : bool) -> list:
		binaryReader = Pure3DBinaryReader(data, isLittleEndian)

		parameter = binaryReader.readPure3DString()
		value = binaryReader.readPure3DMatrix()

		return [ parameter, value ]

	def __init__(
		self, 
		identifier: int = chunkIdentifiers.GAME_ATTRIBUTE_MATRIX_PARAMETER, 
		children : list[Chunk] = None, 
		parameter: str = "", 
		value: mathutils.Matrix = None
	) -> None:
		super().__init__(identifier,children)
	
		self.parameter = parameter
		self.value = mathutils.Matrix() if value is None else value
		
	def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
		binaryWriter.writePure3DString(self.parameter)
		binaryWriter.writePure3DMatrix(self.value)

class GameAttrVectorParameterChunk(Chunk):
	@staticmethod
	def parseData(data : bytes, isLittleEndian : bool) -> list:
		binaryReader = Pure3DBinaryReader(data, isLittleEndian)

		parameter = binaryReader.readPure3DString()
		value = binaryReader.readPure3DVector3()

		return [ parameter, value ]

	def __init__(
		self, 
		identifier: int = chunkIdentifiers.GAME_ATTRIBUTE_VECTOR_PARAMETER, 
		children : list[Chunk] = None, 
		parameter: str = "", 
		value: mathutils.Vector = None
	) -> None:
		super().__init__(identifier,children)
	
		self.parameter = parameter
		self.value = mathutils.Vector() if value is None else value
		
	def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
		binaryWriter.writePure3DString(self.parameter)
		binaryWriter.writePure3DVector3(self.value)

class GameAttrFloatParameterChunk(Chunk):
	@staticmethod
	def parseData(data : bytes, isLittleEndian : bool) -> list:
		binaryReader = Pure3DBinaryReader(data, isLittleEndian)

		parameter = binaryReader.readPure3DString()
		value = binaryReader.readFloat()

		return [ parameter, value ]

	def __init__(
		self, 
		identifier: int = chunkIdentifiers.GAME_ATTRIBUTE_FLOAT_PARAMETER, 
		children : list[Chunk] = None, 
		parameter: str = "", 
		value: float = 0
	) -> None:
		super().__init__(identifier,children)
	
		self.parameter = parameter
		self.value = value
		
	def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
		binaryWriter.writePure3DString(self.parameter)
		binaryWriter.writeFloat(self.value)