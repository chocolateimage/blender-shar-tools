from __future__ import annotations

from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

#
# Class
#

class UnknownChunk(Chunk):
    @staticmethod
    def parseData(data : bytes, isLittleEndian : bool) -> list:
        return [ data ]

    def __init__(
        self, 
        identifier : int, 
        children : list[Chunk] = None, 
        data : bytes = None
    ) -> None:
        super().__init__(identifier, children)

        self.data : bytes = bytes() if data is None else data

    def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
        binaryWriter.writeBytes(self.data)