#
# Imports
#

from __future__ import annotations

import struct

import data.dataSizes

#
# Class
#

class BinaryReader:
    def __init__(self, data : bytes, isLittleEndian : bool = True) -> None:
        self._data = memoryview(data)

        self.isLittleEndian = isLittleEndian

        self._position = 0

        self._byteOrderString = "little" if self.isLittleEndian else "big"

        self._byteOrderSymbol = "<" if self.isLittleEndian else ">"

    def getPosition(self) -> int:
        return self._position

    def getLength(self) -> int:
        return len(self._data)

    def seek(self, position : int) -> None:
        if position < 0 or position >= self.getLength():
            raise ValueError("Seek position out of range.")
        
        self._position = position

    def seekOffset(self, offset : int) -> None:
        self.seek(self._position + offset)

    def readBytes(self, size : int) -> bytes:
        self._checkSize(size)

        valueBytes = self._data[self._position : self._position + size].tobytes()

        self._position += size

        return valueBytes

    def readSByte(self) -> int:
        valueBytes = self.readBytes(data.dataSizes.SBYTE)

        value = int.from_bytes(valueBytes, byteorder = self._byteOrderString, signed = True)

        return value

    def readInt16(self) -> int:
        valueBytes = self.readBytes(data.dataSizes.INT16)

        value = int.from_bytes(valueBytes, byteorder = self._byteOrderString, signed = True)

        return value

    def readInt32(self) -> int:
        valueBytes = self.readBytes(data.dataSizes.INT32)

        value = int.from_bytes(valueBytes, byteorder = self._byteOrderString, signed = True)

        return value

    def readInt64(self) -> int:
        valueBytes = self.readBytes(data.dataSizes.INT64)

        value = int.from_bytes(valueBytes, byteorder = self._byteOrderString, signed = True)

        return value

    def readByte(self) -> int:
        valueBytes = self.readBytes(data.dataSizes.BYTE)

        value = int.from_bytes(valueBytes, byteorder = self._byteOrderString, signed = False)

        return value

    def readUInt16(self) -> int:
        valueBytes = self.readBytes(data.dataSizes.UINT16)

        value = int.from_bytes(valueBytes, byteorder = self._byteOrderString, signed = False)

        return value

    def readUInt32(self) -> int:
        valueBytes = self.readBytes(data.dataSizes.UINT32)

        value = int.from_bytes(valueBytes, byteorder = self._byteOrderString, signed = False)

        return value

    def readUInt64(self) -> int:
        valueBytes = self.readBytes(data.dataSizes.UINT64)

        value = int.from_bytes(valueBytes, byteorder = self._byteOrderString, signed = False)

        return value

    def readFloat(self) -> float:
        valueBytes = self.readBytes(data.dataSizes.FLOAT32)

        value = struct.unpack(self._byteOrderSymbol + "f", valueBytes)[0]

        return value

    def readDouble(self) -> float:
        valueBytes = self.readBytes(data.dataSizes.FLOAT64)

        value = struct.unpack(self._byteOrderSymbol + "d", valueBytes)[0]

        return value

    def readString(self, length : int) -> str:
        valueBytes = self.readBytes(length)

        value = valueBytes.decode("utf-8")

        return value

    def _checkSize(self, neededBytes : int) -> None:
        availableBytes = self.getLength() - self._position

        if neededBytes > availableBytes:
            raise ValueError(f"Operation requires an additional { neededBytes } bytes but only { availableBytes } bytes are available.")