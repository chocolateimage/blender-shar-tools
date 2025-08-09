from __future__ import annotations

from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

#
# Class
#

class CollisionVolumeChunk(Chunk):
    @staticmethod
    def parseData(binaryReader: Pure3DBinaryReader) -> list:
        objectReferenceIndex = binaryReader.readUInt32()
        ownerIndex = binaryReader.readInt32()

        return [ objectReferenceIndex, ownerIndex ]

    def __init__(
        self, 
        identifier: int = chunkIdentifiers.COLLISION_VOLUME, 
        children : list[Chunk] = None, 
        objectReferenceIndex: int = 0,
        ownerIndex: int = 0
    ) -> None:
        super().__init__(identifier,children)
    
        self.objectReferenceIndex = objectReferenceIndex
        self.ownerIndex = ownerIndex
    
    def getNumberOfSubVolumes(self):
        amount = 0
        for i in self.children:
            if i.identifier == self.identifier:
                amount += 1
        return amount
        
    def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
        binaryWriter.writeUInt32(self.objectReferenceIndex)
        binaryWriter.writeInt32(self.ownerIndex)
        binaryWriter.writeUInt32(self.getNumberOfSubVolumes())