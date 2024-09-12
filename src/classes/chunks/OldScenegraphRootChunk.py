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

class OldScenegraphRootChunk(Chunk):
    def __init__(
        self, 
        identifier: int = chunkIdentifiers.OLD_SCENEGRAPH_ROOT, 
        children: list[Chunk] = None,
    ) -> None:
        super().__init__(identifier, children)