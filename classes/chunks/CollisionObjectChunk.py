from __future__ import annotations

from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

#
# Class
#

class CollisionObjectChunk(Chunk):
    @staticmethod
    def parseData(binaryReader: Pure3DBinaryReader) -> list:
        name = binaryReader.readPure3DString()
        version = binaryReader.readUInt32()
        materialName = binaryReader.readPure3DString()
        numberOfSubObjects = binaryReader.readUInt32()

        return [ name, version, materialName, numberOfSubObjects ]

    def __init__(
        self, 
        identifier: int = chunkIdentifiers.COLLISION_OBJECT, 
        children : list[Chunk] = None, 
        name: str = "",
        version: int = 0,
        materialName: str = "",
        numberOfSubObjects: int = 0
    ) -> None:
        super().__init__(identifier,children)
    
        self.name = name
        self.version = version
        self.materialName = materialName
        self.numberOfSubObjects = numberOfSubObjects
        
    def getNumberOfOwners(self):
        amount = 0
        for i in self.children:
            if i.identifier == chunkIdentifiers.COLLISION_VOLUME_OWNER:
                amount += 1
        return amount

    def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
        binaryWriter.writePure3DString(self.name)
        binaryWriter.writeUInt32(self.version)
        binaryWriter.writePure3DString(self.materialName)
        binaryWriter.writeUInt32(self.numberOfSubObjects)
        binaryWriter.writeUInt32(self.getNumberOfOwners())