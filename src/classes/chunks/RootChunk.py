#
# Imports
#

from __future__ import annotations

from classes.chunks.Chunk import Chunk

#
# Class
#

class RootChunk(Chunk):
    def __init__(
        self, 
        identifier : int, 
        children : list[Chunk] = None, 
        isNewFile : bool = False
    ) -> None:
        super().__init__(identifier, children)

        self.isNewFile : bool = isNewFile