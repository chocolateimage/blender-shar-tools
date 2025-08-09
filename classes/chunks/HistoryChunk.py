from __future__ import annotations

from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

#
# Class
#

class HistoryChunk(Chunk):
    @staticmethod
    def parseData(binaryReader: Pure3DBinaryReader) -> list:
        
        numberOfLines = binaryReader.readUInt16()

        lines : list[str] = []

        for i in range(numberOfLines):
            lines.append(binaryReader.readPure3DString())

        return [ lines ]

    def __init__(
        self, 
        identifier : int = chunkIdentifiers.HISTORY, 
        children : list[Chunk] = None, 
        lines : list[str] = None
    ) -> None:
        super().__init__(chunkIdentifiers.HISTORY)

        self.lines : list[str] = [] if lines is None else lines

    def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
        binaryWriter.writeUInt16(len(self.lines))

        for line in self.lines:
            binaryWriter.writePure3DString(line)