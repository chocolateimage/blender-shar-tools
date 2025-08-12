from __future__ import annotations

from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers


class CompositeDrawablePropChunk(Chunk):
    @staticmethod
    def parseData(binaryReader: Pure3DBinaryReader) -> list:
        name = binaryReader.readPure3DString()
        isTranslucent = binaryReader.readUInt32()
        skeletonJointId = binaryReader.readUInt32()

        return [ name, isTranslucent, skeletonJointId ]

    def __init__(
        self, 
        identifier: int = chunkIdentifiers.COMPOSITE_DRAWABLE_PROP, 
        children: list[Chunk] = None,
        name: str = "",
        isTranslucent: int = 0,
        skeletonJointId: int = 0
    ) -> None:
        super().__init__(identifier, children)

        self.name = name
        self.isTranslucent = isTranslucent
        self.skeletonJointId = skeletonJointId

    def writeData(self, binaryWriter: Pure3DBinaryWriter) -> None:
        binaryWriter.writePure3DString(self.name)
        binaryWriter.writeUInt32(self.isTranslucent)
        binaryWriter.writeUInt32(self.skeletonJointId)
