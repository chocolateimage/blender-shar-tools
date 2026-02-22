from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

class AnimationChunk(Chunk):
    @staticmethod
    def parseData(binaryReader: Pure3DBinaryReader) -> list:
        version = binaryReader.readUInt32()
        name = binaryReader.readPure3DString()
        animationType = binaryReader.readPure3DFourCharacterCode()
        numberOfFrames = binaryReader.readFloat()
        frameRate = binaryReader.readFloat()
        cyclic = binaryReader.readUInt32()
        
        return [version, name, animationType, numberOfFrames, frameRate, cyclic]

    def __init__(
        self, 
        identifier: int = chunkIdentifiers.ANIMATION, 
        children: list[Chunk] = None,
        version: int = 0,
        name: str = "",
        animationType: str = "",
        numberOfFrames: float = 0,
        frameRate: float = 0,
        cyclic: int = 0,
    ) -> None:
        super().__init__(identifier, children)
    
        self.version = version
        self.name = name
        self.animationType = animationType
        self.numberOfFrames = numberOfFrames
        self.frameRate = frameRate
        self.cyclic = cyclic

    def writeData(self, binaryWriter: Pure3DBinaryWriter) -> None:
        binaryWriter.writeUInt32(self.version)
        binaryWriter.writePure3DString(self.name)
        binaryWriter.writePure3DFourCharacterCode(self.animationType)
        binaryWriter.writeFloat(self.numberOfFrames)
        binaryWriter.writeFloat(self.frameRate)
        binaryWriter.writeUInt32(self.cyclic)
