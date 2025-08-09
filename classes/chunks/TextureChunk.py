from __future__ import annotations

from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

#
# Class
#

class TextureChunk(Chunk):
    @staticmethod
    def parseData(binaryReader: Pure3DBinaryReader) -> list:
        name = binaryReader.readPure3DString()
        version = binaryReader.readUInt32()
        width = binaryReader.readUInt32()
        height = binaryReader.readUInt32()
        bitsPerPixel = binaryReader.readUInt32()
        alphaDepth = binaryReader.readUInt32()
        numberOfMipMaps = binaryReader.readUInt32()
        textureType = binaryReader.readUInt32()
        usage = binaryReader.readUInt32()
        priority = binaryReader.readUInt32()

        return [ name, version, width, height, bitsPerPixel, alphaDepth, numberOfMipMaps, textureType, usage, priority ]

    def __init__(
        self, 
        identifier: int = chunkIdentifiers.TEXTURE, 
        children : list[Chunk] = None, 
        name: str = "", 
        version: int = 0, 
        width: int = 0, 
        height: int = 0, 
        bitsPerPixel: int = 0, 
        alphaDepth: int = 0, 
        numberOfMipMaps: int = 0, 
        textureType: int = 0, 
        usage: int = 0, 
        priority: int = 0
    ) -> None:
        super().__init__(identifier,children)
    
        self.name = name
        self.version = version
        self.width = width
        self.height = height
        self.bitsPerPixel = bitsPerPixel
        self.alphaDepth = alphaDepth
        self.numberOfMipMaps = numberOfMipMaps
        self.textureType = textureType
        self.usage = usage
        self.priority = priority

    def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
        binaryWriter.writePure3DString(self.name)
        binaryWriter.writeUInt32(self.version)
        binaryWriter.writeUInt32(self.width)
        binaryWriter.writeUInt32(self.height)
        binaryWriter.writeUInt32(self.bitsPerPixel)
        binaryWriter.writeUInt32(self.alphaDepth)
        binaryWriter.writeUInt32(self.numberOfMipMaps)
        binaryWriter.writeUInt32(self.textureType)
        binaryWriter.writeUInt32(self.usage)
        binaryWriter.writeUInt32(self.priority)