from __future__ import annotations

from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers


class CompositeDrawableSkinListChunk(Chunk):
    def __init__(
        self, 
        identifier: int = chunkIdentifiers.COMPOSITE_DRAWABLE_SKIN_LIST, 
        children: list[Chunk] = None,
    ) -> None:
        super().__init__(identifier, children)

    def getNumberOfElements(self):
        amount = 0
        for i in self.children:
            if i.identifier == chunkIdentifiers.COMPOSITE_DRAWABLE_SKIN:
                amount += 1
        return amount

    def writeData(self, binaryWriter: Pure3DBinaryWriter) -> None:
        binaryWriter.writeUInt32(self.getNumberOfElements())
