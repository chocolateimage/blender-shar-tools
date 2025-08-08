from __future__ import annotations

from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

from classes.Colour import Colour

import data.chunkIdentifiers as chunkIdentifiers

#
# Class
#

class ColourListChunk(Chunk):
    @staticmethod
    def parseData(data : bytes, isLittleEndian : bool) -> list:
        binaryReader = Pure3DBinaryReader(data, isLittleEndian)

        numberOfColours = binaryReader.readUInt32()
        
        colours = []
        
        for i in range(numberOfColours):
            colours.append(binaryReader.readPure3DColour())
        
        return [ colours ]

    def __init__(
        self, 
        identifier: int = chunkIdentifiers.COLOUR_LIST, 
        children: list[Chunk] = None, 
        colours: list[Colour] = None
    ) -> None:
        super().__init__(identifier, children)
    
        self.colours = [] if colours is None else colours

    def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
        binaryWriter.writeUInt32(len(self.colours))

        for colour in self.colours:
            binaryWriter.writePure3DColour(colour)