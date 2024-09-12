#
# Imports
#

from __future__ import annotations

from classes.chunks.Chunk import Chunk

import data.chunkIdentifiers as chunkIdentifiers

#
# Class
#

class FenceChunk(Chunk):
    def __init__(
        self, 
        identifier : int = chunkIdentifiers.FENCE, 
        children : list[Chunk] = None
    ) -> None:
        super().__init__(chunkIdentifiers.FENCE, children)