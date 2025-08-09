from __future__ import annotations

from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

#
# Class
#

class CollisionEffectChunk(Chunk):
    @staticmethod
    def parseData(binaryReader: Pure3DBinaryReader) -> list:
        classType = binaryReader.readUInt32()
        phyPropID = binaryReader.readUInt32()
        soundResourceDataName = binaryReader.readPure3DString()

        return [
            classType,
            phyPropID,
            soundResourceDataName,
        ]

    def __init__(
        self, 
        identifier: int = chunkIdentifiers.COLLISION_EFFECT, 
        children : list[Chunk] = None, 
        classType: int = 0,
        phyPropID: int = 0,
        soundResourceDataName: str = "",
    ) -> None:
        super().__init__(identifier,children)
    
        self.classType = classType
        self.phyPropID = phyPropID
        self.soundResourceDataName = soundResourceDataName

    def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
        binaryWriter.writeUInt32(self.classType)
        binaryWriter.writeUInt32(self.phyPropID)
        binaryWriter.writePure3DString(self.soundResourceDataName)