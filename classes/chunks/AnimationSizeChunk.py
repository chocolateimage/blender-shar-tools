from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

class AnimationSizeChunk(Chunk):
    @staticmethod
    def parseData(binaryReader: Pure3DBinaryReader) -> list:
        version = binaryReader.readUInt32()
        pc = binaryReader.readUInt32()
        ps2 = binaryReader.readUInt32()
        xbox = binaryReader.readUInt32()
        gc = binaryReader.readUInt32()
        
        return [version, pc, ps2, xbox, gc]

    def __init__(
        self, 
        identifier: int = chunkIdentifiers.ANIMATION_SIZE, 
        children: list[Chunk] = None,
        version: int = 0,
        pc: int = 0,
        ps2: int = 0,
        xbox: int = 0,
        gc: int = 0,
    ) -> None:
        super().__init__(identifier, children)
    
        self.version = version
        self.pc = pc
        self.ps2 = ps2
        self.xbox = xbox
        self.gc = gc

    def writeData(self, binaryWriter: Pure3DBinaryWriter) -> None:
        binaryWriter.writeUInt32(self.version)
        binaryWriter.writeUInt32(self.pc)
        binaryWriter.writeUInt32(self.ps2)
        binaryWriter.writeUInt32(self.xbox)
        binaryWriter.writeUInt32(self.gc)
