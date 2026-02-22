from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

import mathutils

class Vector3DOFChannelChunk(Chunk):
    @staticmethod
    def parseData(binaryReader: Pure3DBinaryReader) -> list:
        version = binaryReader.readUInt32()
        param = binaryReader.readPure3DFourCharacterCode()
        numFrames = binaryReader.readUInt32()
        frames = []
        values = []

        for _ in range(numFrames):
            frames.append(binaryReader.readUInt16())

        for _ in range(numFrames):
            values.append(binaryReader.readPure3DVector3())
        
        return [version, param, frames, values]

    def __init__(
        self, 
        identifier: int = chunkIdentifiers.VECTOR_3D_OF_CHANNEL, 
        children: list[Chunk] = None,
        version: int = 0,
        param: str = "",
        frames: list[int] = None,
        values: list[mathutils.Vector] = None,
    ) -> None:
        super().__init__(identifier, children)
    
        self.version = version
        self.param = param
        self.frames = [] if frames is None else frames
        self.values = [] if values is None else values

    def writeData(self, binaryWriter: Pure3DBinaryWriter) -> None:
        binaryWriter.writeUInt32(self.version)
        binaryWriter.writePure3DFourCharacterCode(self.param)

        if len(self.frames) != len(self.values):
            raise Exception("Frame count does not match value count")

        binaryWriter.writeUInt32(len(self.frames))

        for frame in self.frames:
            binaryWriter.writeUInt16(frame)
        
        for value in self.values:
            binaryWriter.writePure3DVector3(value)
