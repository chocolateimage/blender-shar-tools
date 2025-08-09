from __future__ import annotations

from classes.chunks.Chunk import Chunk

#
# Class
#

class UnknownChunk(Chunk):
    def __init__(
        self, 
        identifier : int, 
        children : list[Chunk] = None
    ) -> None:
        super().__init__(identifier, children)
