from __future__ import annotations

from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers


class CompositeDrawableChunk(Chunk):
    @staticmethod
    def parseData(binaryReader: Pure3DBinaryReader) -> list:
        name = binaryReader.readPure3DString()
        skeletonName = binaryReader.readPure3DString()
        
        return [name, skeletonName]

    def __init__(
        self, 
        identifier: int = chunkIdentifiers.COMPOSITE_DRAWABLE, 
        children: list[Chunk] = None,
        name: str = "",
        skeletonName: str = "",
    ) -> None:
        super().__init__(identifier, children)
    
        self.name = name
        self.skeletonName = skeletonName

    def writeData(self, binaryWriter: Pure3DBinaryWriter) -> None:
        binaryWriter.writePure3DString(self.name)

        binaryWriter.writePure3DString(self.skeletonName)
