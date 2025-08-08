from __future__ import annotations

from classes.chunks.Chunk import Chunk
from classes.chunks.UnknownChunk import UnknownChunk

#
# Class
#

class ChunkRegistry:
    def __init__(self, chunkRegistry : ChunkRegistry | None = None) -> None:
        self.chunkClasses = {} 
        
        if chunkRegistry is not None:
            self.chunkClasses = chunkRegistry.chunkClasses

    def getClass(self, chunkIdentifier : int) -> Chunk:
        if chunkIdentifier in self.chunkClasses:
            return self.chunkClasses[chunkIdentifier]
        else:
            return UnknownChunk

    def register(self, chunkIdentifier : int, chunkClass : Chunk) -> None:
        self.chunkClasses[chunkIdentifier] = chunkClass