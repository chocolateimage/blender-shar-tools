from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

class AnimationGroupListChunk(Chunk):
    @staticmethod
    def parseData(binaryReader: Pure3DBinaryReader) -> list:
        version = binaryReader.readUInt32()
        
        return [version]

    def __init__(
        self, 
        identifier: int = chunkIdentifiers.ANIMATION_GROUP_LIST, 
        children: list[Chunk] = None,
        version: int = 0,
    ) -> None:
        super().__init__(identifier, children)
    
        self.version = version

    def writeData(self, binaryWriter: Pure3DBinaryWriter) -> None:
        binaryWriter.writeUInt32(self.version)
        binaryWriter.writeUInt32(len(self.children))
