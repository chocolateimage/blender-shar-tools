#
# Imports
#

from __future__ import annotations

from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

#
# Class
#

class ImageDataChunk(Chunk):
    @staticmethod
    def parseData(data : bytes, isLittleEndian : bool) -> list:
        binaryReader = Pure3DBinaryReader(data, isLittleEndian)

        imageDataLength = binaryReader.readUInt32()
        imageData = binaryReader.readBytes(imageDataLength)

        return [ imageData ]

    def __init__(
        self, 
        identifier: int = chunkIdentifiers.IMAGE_DATA, 
        children: list[Chunk] = None, 
        imageData: bytes = None
    ) -> None:
        super().__init__(chunkIdentifiers.IMAGE_DATA,children)
    
        self.imageData = bytes() if imageData is None else imageData

    def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
        binaryWriter.writeUInt32(len(self.imageData))
        binaryWriter.writeBytes(self.imageData)