from __future__ import annotations

from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

#
# Class
#

class PhysicsObjectChunk(Chunk):
    @staticmethod
    def parseData(binaryReader: Pure3DBinaryReader) -> list:
        name = binaryReader.readPure3DString()
        version = binaryReader.readUInt32()
        materialName = binaryReader.readPure3DString()
        numJoints = binaryReader.readUInt32()
        volume = binaryReader.readFloat()
        restingSensitivity = binaryReader.readFloat()

        return [
            name,
            version,
            materialName,
            numJoints,
            volume,
            restingSensitivity
        ]

    def __init__(
        self, 
        identifier: int = chunkIdentifiers.PHYSICS_OBJECT, 
        children : list[Chunk] = None, 
        name: str = "",
        version: int = 1,
        materialName: str = "",
        numJoints: int = 0,
        volume: float = 1,
        restingSensitivity: float = 1
    ) -> None:
        super().__init__(identifier,children)
    
        self.name = name
        self.version = version
        self.materialName = materialName
        self.numJoints = numJoints
        self.volume = volume
        self.restingSensitivity = restingSensitivity

    def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
        binaryWriter.writePure3DString(self.name)
        binaryWriter.writeUInt32(self.version)
        binaryWriter.writePure3DString(self.materialName)
        binaryWriter.writeUInt32(self.numJoints)
        binaryWriter.writeFloat(self.volume)
        binaryWriter.writeFloat(self.restingSensitivity)