#
# Imports
#

import struct

import data.dataSizes

#
# Class
#

class BinaryReader:
	def __init__(self, data : bytes, isLittleEndian : bool) -> None:
		self.data = memoryview(data)

		self.isLittleEndian = isLittleEndian

		self.byteOrderString = "little" if self.isLittleEndian else "big"

		self.byteOrderSymbol = "<" if self.isLittleEndian else ">"

		self.position = 0

	def getPosition(self) -> int:
		return self.position

	def getLength(self) -> int:
		return len(self.data)

	def readBytes(self, size : int) -> bytes:
		self.checkSize(size)

		valueBytes = self.data[self.position : self.position + size].tobytes()

		self.position += size

		return valueBytes

	def readFloat32(self) -> float:
		self.checkSize(data.dataSizes.FLOAT32)

		valueBytes = self.readBytes(data.dataSizes.FLOAT32)

		value = struct.unpack(self.byteOrderSymbol + "f", valueBytes)[0]

		self.position += data.dataSizes.FLOAT32

		return value

	# TODO: readFloat64 (idk how python handles 64-bit floats)

	def readInt8(self) -> int:
		self.checkSize(data.dataSizes.INT8)

		valueBytes = self.readBytes(data.dataSizes.INT8)

		value = int.from_bytes(valueBytes, byteorder = self.byteOrderString, signed = True)

		self.position += data.dataSizes.INT8

		return value

	def readInt16(self) -> int:
		self.checkSize(data.dataSizes.INT16)

		valueBytes = self.readBytes(data.dataSizes.INT16)

		value = int.from_bytes(valueBytes, byteorder = self.byteOrderString, signed = True)

		self.position += data.dataSizes.INT16

		return value

	def readInt32(self) -> int:
		self.checkSize(data.dataSizes.INT32)

		valueBytes = self.readBytes(data.dataSizes.INT32)

		value = int.from_bytes(valueBytes, byteorder = self.byteOrderString, signed = True)

		self.position += data.dataSizes.INT32

		return value

	# TODO: readInt64 (idk how python handles 64-bit integers)

	def readString(self, length : int) -> str:
		valueBytes = self.readBytes(length)

		value = valueBytes.decode("utf-8")

		return value

	def readUint8(self) -> int:
		self.checkSize(data.dataSizes.UINT8)

		valueBytes = self.readBytes(data.dataSizes.UINT8)

		value = int.from_bytes(valueBytes, byteorder = self.byteOrderString, signed = False)

		self.position += data.dataSizes.UINT8

		return value

	def readUint16(self) -> int:
		self.checkSize(data.dataSizes.UINT16)

		valueBytes = self.readBytes(data.dataSizes.UINT16)

		value = int.from_bytes(valueBytes, byteorder = self.byteOrderString, signed = False)

		self.position += data.dataSizes.UINT16

		return value

	def readUint32(self) -> int:
		self.checkSize(data.dataSizes.UINT32)

		valueBytes = self.readBytes(data.dataSizes.UINT32)

		value = int.from_bytes(valueBytes, byteorder = self.byteOrderString, signed = False)

		self.position += data.dataSizes.UINT32

		return value

	# TODO: readUint64 (idk how python handles 64-bit integers)

	def seek(self, position : int) -> None:
		if position < 0 or position >= self.getLength():
			raise ValueError("Seek position out of range.")
		
		self.position = position

	def seekOffset(self, offset : int) -> None:
		self.seek(self.position + offset)

	def checkSize(self, neededBytes : int) -> None:
		availableBytes = self.getLength() - self.position

		if neededBytes > availableBytes:
			raise ValueError(f"Operation requires an additional { neededBytes } bytes but only { availableBytes } bytes are available.")