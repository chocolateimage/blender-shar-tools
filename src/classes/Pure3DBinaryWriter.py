#
# Imports
#

from __future__ import annotations

import math
import mathutils

from classes.BinaryWriter import BinaryWriter
from classes.Colour import Colour
from classes.SymmetricMatrix3x3 import SymmetricMatrix3x3

#
# Class
#

class Pure3DBinaryWriter(BinaryWriter):
	def writePure3DColour(self, colour : Colour) -> None:
		if self.isLittleEndian:
			self.writeByte(colour.blue)

			self.writeByte(colour.green)

			self.writeByte(colour.red)

			self.writeByte(colour.alpha)
		else:
			self.writeByte(colour.alpha)

			self.writeByte(colour.red)

			self.writeByte(colour.green)

			self.writeByte(colour.blue)

	def writePure3DFourCharacterCode(self, value : str) -> None:
		if len(value) > 4:
			raise ValueError("Four character code must be less than or equal to 4 characters.")

		paddedValue = value.ljust(4, "\0")

		if not self.isLittleEndian:
			paddedValueCharacters = list(paddedValue)

			paddedValueCharacters.reverse()

			paddedValue = "".join(paddedValueCharacters)

		self.writeString(paddedValue)

	def writePure3DMatrix(self, matrix : mathutils.Matrix) -> None:
		self.writeFloat(matrix[0][0])

		self.writeFloat(matrix[0][1])

		self.writeFloat(matrix[0][2])

		self.writeFloat(matrix[0][3])

		self.writeFloat(matrix[1][0])

		self.writeFloat(matrix[1][1])

		self.writeFloat(matrix[1][2])

		self.writeFloat(matrix[1][3])

		self.writeFloat(matrix[2][0])

		self.writeFloat(matrix[2][1])

		self.writeFloat(matrix[2][2])

		self.writeFloat(matrix[2][3])

		self.writeFloat(matrix[3][0])

		self.writeFloat(matrix[3][1])

		self.writeFloat(matrix[3][2])

		self.writeFloat(matrix[3][3])

	def writeSymmetricMatrix3x3(self, matrix: SymmetricMatrix3x3):
		self.writeFloat(matrix.xx)
		self.writeFloat(matrix.xy)
		self.writeFloat(matrix.xz)
		self.writeFloat(matrix.yy)
		self.writeFloat(matrix.yz)
		self.writeFloat(matrix.zz)

	def writePure3DString(self, value : str) -> None:
		if len(value) > 255:
			raise ValueError("String must be less than or equal to 255 characters.")

		valueToWrite = value
		
		if len(value) < 252:
			# Note: This padding is intentionally fucked (doesn't include the length byte)
			#	because Radical was stupid when they were making The Simpsons Hit & Run
			valueToWrite = value.ljust(4 * math.ceil(len(value) / 4), "\0")

		self.writeByte(len(valueToWrite))

		self.writeString(valueToWrite)

	def writePure3DVector2(self, vector2 : mathutils.Vector) -> None:
		self.writeFloat(vector2.x)

		self.writeFloat(vector2.y)

	def writePure3DVector3(self, vector3 : mathutils.Vector) -> None:
		self.writeFloat(vector3.x)

		self.writeFloat(vector3.y)

		self.writeFloat(vector3.z)