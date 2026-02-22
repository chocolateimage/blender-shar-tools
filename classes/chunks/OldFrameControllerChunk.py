from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

class OldFrameController(Chunk):
    @staticmethod
    def parseData(binaryReader: Pure3DBinaryReader) -> list:
        version = binaryReader.readUInt32()
        name = binaryReader.readPure3DString()
        type = binaryReader.readPure3DFourCharacterCode()
        frameOffset = binaryReader.readFloat()
        hierarchyName = binaryReader.readPure3DString()
        animationName = binaryReader.readPure3DString()
        
        return [version, name, type, frameOffset, hierarchyName, animationName]

    def __init__(
        self, 
        identifier: int = chunkIdentifiers.OLD_FRAME_CONTROLLER, 
        children: list[Chunk] = None,
        version: int = 0,
        name: str = "",
        type: str = "",
        frameOffset: float = 0,
        hierarchyName: str = "",
        animationName: str = "",
    ) -> None:
        super().__init__(identifier, children)
    
        self.version = version
        self.name = name
        self.type = type
        self.frameOffset = frameOffset
        self.hierarchyName = hierarchyName
        self.animationName = animationName

    def writeData(self, binaryWriter: Pure3DBinaryWriter) -> None:
        binaryWriter.writePure3DString(self.name)
        binaryWriter.writeUInt32(self.version)
        binaryWriter.writePure3DFourCharacterCode(self.type)
        binaryWriter.writeFloat(self.frameOffset)
        binaryWriter.writePure3DString(self.hierarchyName)
        binaryWriter.writePure3DString(self.animationName)
