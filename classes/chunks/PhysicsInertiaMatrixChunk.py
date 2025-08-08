#
# Imports
#

from __future__ import annotations

from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

from classes.SymmetricMatrix3x3 import SymmetricMatrix3x3

#
# Class
#

class PhysicsInertiaMatrixChunk(Chunk):
    @staticmethod
    def parseData(data : bytes, isLittleEndian : bool) -> list:
        binaryReader = Pure3DBinaryReader(data, isLittleEndian)

        matrix = binaryReader.readSymmetricMatrix3x3()

        return [
            matrix
        ]

    def __init__(
        self, 
        identifier: int = chunkIdentifiers.PHYSICS_INERTIA_MATRIX, 
        children : list[Chunk] = None, 
        matrix: SymmetricMatrix3x3 = None
    ) -> None:
        super().__init__(identifier,children)
    
        self.matrix = SymmetricMatrix3x3() if matrix is None else matrix

    def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
        binaryWriter.writeSymmetricMatrix3x3(self.matrix)