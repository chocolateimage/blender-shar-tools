from __future__ import annotations

from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

#
# Class
#

class CollisionObjectAttributeChunk(Chunk):
    @staticmethod
    def parseData(data : bytes, isLittleEndian : bool) -> list:
        binaryReader = Pure3DBinaryReader(data, isLittleEndian)

        staticAttribute = binaryReader.readUInt16()
        defaultArea = binaryReader.readUInt32()
        canRoll = binaryReader.readUInt16()
        canSlide = binaryReader.readUInt16()
        canSpin = binaryReader.readUInt16()
        canBounce = binaryReader.readUInt16()
        extraAttribute1 = binaryReader.readUInt32()
        extraAttribute2 = binaryReader.readUInt32()
        extraAttribute3 = binaryReader.readUInt32()

        return [
            staticAttribute,
            defaultArea,
            canRoll,
            canSlide,
            canSpin,
            canBounce,
            extraAttribute1,
            extraAttribute2,
            extraAttribute3,
        ]

    def __init__(
        self, 
        identifier: int = chunkIdentifiers.COLLISION_OBJECT_ATTRIBUTE, 
        children : list[Chunk] = None, 
        staticAttribute: int = 0,
        defaultArea: int = 0,
        canRoll: int = 0,
        canSlide: int = 0,
        canSpin: int = 0,
        canBounce: int = 0,
        extraAttribute1: int = 0,
        extraAttribute2: int = 0,
        extraAttribute3: int = 0,
    ) -> None:
        super().__init__(identifier,children)
    
        self.staticAttribute = staticAttribute
        self.defaultArea = defaultArea
        self.canRoll = canRoll
        self.canSlide = canSlide
        self.canSpin = canSpin
        self.canBounce = canBounce
        self.extraAttribute1 = extraAttribute1
        self.extraAttribute2 = extraAttribute2
        self.extraAttribute3 = extraAttribute3

    def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
        binaryWriter.writeUInt16(self.staticAttribute)
        binaryWriter.writeUInt32(self.defaultArea)
        binaryWriter.writeUInt16(self.canRoll)
        binaryWriter.writeUInt16(self.canSlide)
        binaryWriter.writeUInt16(self.canSpin)
        binaryWriter.writeUInt16(self.canBounce)
        binaryWriter.writeUInt32(self.extraAttribute1)
        binaryWriter.writeUInt32(self.extraAttribute2)
        binaryWriter.writeUInt32(self.extraAttribute3)