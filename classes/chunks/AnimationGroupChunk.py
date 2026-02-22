from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

class AnimationGroupChunk(Chunk):
    @staticmethod
    def parseData(binaryReader: Pure3DBinaryReader) -> list:
        version = binaryReader.readUInt32()
        name = binaryReader.readPure3DString()
        groupIdentifier = binaryReader.readUInt32()
        
        return [version, name, groupIdentifier]

    def __init__(
        self, 
        identifier: int = chunkIdentifiers.ANIMATION_GROUP, 
        children: list[Chunk] = None,
        version: int = 0,
        name: str = "",
        groupIdentifier = 0,
    ) -> None:
        super().__init__(identifier, children)
    
        self.version = version
        self.name = name
        self.groupIdentifier = groupIdentifier

    def writeData(self, binaryWriter: Pure3DBinaryWriter) -> None:
        binaryWriter.writeUInt32(self.version)
        binaryWriter.writePure3DString(self.name)
        binaryWriter.writeUInt32(self.groupIdentifier)
        binaryWriter.writeUInt32(len(self.children))
