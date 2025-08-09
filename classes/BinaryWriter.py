from __future__ import annotations

import struct

import data.dataSizes

#
# Class
#

class BinaryWriter:
    def __init__(self, isLittleEndian : bool = True) -> None:
        self.isLittleEndian : bool = isLittleEndian

        self._byteArray : bytearray = bytearray()

        self._length : int = 0

        self.position : int = 0

        self._byteOrderString = "little" if self.isLittleEndian else "big"

        self._byteOrderSymbol = "<" if self.isLittleEndian else ">"

    def getBytes(self) -> bytes:
        return bytes(self._byteArray[:self._length])

    def getPosition(self) -> int:
        return self.position

    def getLength(self) -> int:
        return self._length

    def seek(self, pos : int) -> None:
        self.position = pos

    def seekOffset(self, offset : int) -> None:
        self.seek(self.position + offset)

    def writeBytes(self, data : bytes) -> None:
        dataLength = len(data)

        self._byteArray[self.position:self.position + dataLength] = data

        self.position += dataLength

        self._length = max(self._length, self.position)

    def writeSByte(self, value : int) -> None:
        valueBytes = value.to_bytes(data.dataSizes.SBYTE, byteorder = self._byteOrderString, signed = True)

        self.writeBytes(valueBytes)

    def writeInt16(self, value : int) -> None:
        valueBytes = value.to_bytes(data.dataSizes.INT16, byteorder = self._byteOrderString, signed = True)

        self.writeBytes(valueBytes)

    def writeInt32(self, value : int) -> None:
        valueBytes = value.to_bytes(data.dataSizes.INT32, byteorder = self._byteOrderString, signed = True)

        self.writeBytes(valueBytes)

    def writeInt64(self, value : int) -> None:
        valueBytes = value.to_bytes(data.dataSizes.INT64, byteorder = self._byteOrderString, signed = True)

        self.writeBytes(valueBytes)

    def writeByte(self, value : int) -> None:
        valueBytes = value.to_bytes(data.dataSizes.BYTE, byteorder = self._byteOrderString, signed = False)

        self.writeBytes(valueBytes)

    def writeUInt8(self, value : int) -> None:
        valueBytes = value.to_bytes(data.dataSizes.UINT8, byteorder = self._byteOrderString, signed = False)

        self.writeBytes(valueBytes)

    def writeUInt16(self, value : int) -> None:
        valueBytes = value.to_bytes(data.dataSizes.UINT16, byteorder = self._byteOrderString, signed = False)

        self.writeBytes(valueBytes)

    def writeUInt32(self, value : int) -> None:
        valueBytes = value.to_bytes(data.dataSizes.UINT32, byteorder = self._byteOrderString, signed = False)

        self.writeBytes(valueBytes)

    def writeUInt64(self, value : int) -> None:
        valueBytes = value.to_bytes(data.dataSizes.UINT64, byteorder = self._byteOrderString, signed = False)

        self.writeBytes(valueBytes)

    def writeFloat(self, value : float) -> None:
        valueBytes = struct.pack(self._byteOrderSymbol + "f", value)

        self.writeBytes(valueBytes)

    def writeDouble(self, value : float) -> None:
        valueBytes = struct.pack(self._byteOrderSymbol + "d", value)

        self.writeBytes(valueBytes)

    def writeString(self, value : str) -> None:
        valueBytes = value.encode("utf-8")

        self.writeBytes(valueBytes)
