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

class OldPrimitiveGroupChunk(Chunk):

    primitiveTypes = {
        "TRIANGLE_LIST": 0,
        "TRIANGLE_STRIP": 1,
        "LINE_LIST": 2,
        "LINE_STRIP": 3,
    }

    vertexTypes = {
        "UVS": 1,
        "UVS_2": 2,
        "UVS_3": 3,
        "UVS_4": 4,
        "UVS_5": 5,
        "UVS_6": 6,
        "UVS_7": 7,
        "UVS_8": 8,
        "NORMALS": 1 << 4,
        "COLOURS": 1 << 5,
        "SPECULAR": 1 << 6,
        "MATRICES": 1 << 7,
        "WEIGHTS": 1 << 8,
        "SIZE": 1 << 9,
        "W": 1 << 10,
        "BI_NORMAL": 1 << 11,
        "TANGENT": 1 << 12,
        "POSITION": 1 << 13,
        "COLOUR_2": 1 << 14,
        "COLOUR_COUNT_1": 1 << 15,
        "COLOUR_COUNT_2": 2 << 15,
        "COLOUR_COUNT_3": 3 << 15,
        "COLOUR_COUNT_4": 4 << 15,
        "COLOUR_COUNT_5": 5 << 15,
        "COLOUR_COUNT_6": 6 << 15,
        "COLOUR_COUNT_7": 7 << 15,
        "COLOUR_MASK": 7 << 15,
        "COLOUR_MASK_OFFSET": 15,
    }

    vertexTypeMap = {
        chunkIdentifiers.PACKED_NORMAL_LIST: vertexTypes["NORMALS"],
        chunkIdentifiers.NORMAL_LIST: vertexTypes["NORMALS"],
        chunkIdentifiers.COLOUR_LIST: vertexTypes["COLOURS"],
        chunkIdentifiers.MATRIX_LIST: vertexTypes["MATRICES"],
        chunkIdentifiers.MATRIX_PALETTE: vertexTypes["MATRICES"],
        chunkIdentifiers.WEIGHT_LIST: vertexTypes["WEIGHTS"],
        chunkIdentifiers.POSITION_LIST: vertexTypes["POSITION"],
    }

    uvTypeMap = [
        vertexTypes["UVS"],
        vertexTypes["UVS_2"],
        vertexTypes["UVS_3"],
        vertexTypes["UVS_4"],
        vertexTypes["UVS_5"],
        vertexTypes["UVS_6"],
        vertexTypes["UVS_7"],
        vertexTypes["UVS_8"],
    ]

    @staticmethod
    def parseData(data : bytes, isLittleEndian : bool) -> list:
        binaryReader = Pure3DBinaryReader(data, isLittleEndian)

        version = binaryReader.readUInt32()
        shaderName = binaryReader.readPure3DString()
        primitiveType = binaryReader.readUInt32()

        # Note: This is the Vertex Type, this is not stored
        #      because it is determined when writing the chunk.
        binaryReader.readUInt32()

        numberOfVertices = binaryReader.readUInt32()
        numberOfIndices = binaryReader.readUInt32()
        numberOfMatrices = binaryReader.readUInt32()

        return [ version, shaderName, primitiveType, numberOfVertices, numberOfIndices, numberOfMatrices ]

    def __init__(
        self, 
        identifier: int = chunkIdentifiers.OLD_PRIMITIVE_GROUP, 
        children : list[Chunk] = None, 
        version: int = 0, 
        shaderName: str = "", 
        primitiveType: str = "", 
        numberOfVertices: int = 0, 
        numberOfIndices: int = 0, 
        numberOfMatrices: int = 0
    ) -> None:
        super().__init__(identifier,children)
        
        self.version = version
        self.shaderName = shaderName
        self.primitiveType = primitiveType
        self.numberOfVertices = numberOfVertices
        self.numberOfIndices = numberOfIndices
        self.numberOfMatrices = numberOfMatrices
    
    def getVertexType(self) -> int:
        vertexType = 0
        
        uvListCount = 0
    
        for chunk in self.children:
            if chunk.identifier == chunkIdentifiers.UV_LIST:
                uvListCount += 1
            else:
                if chunk.identifier in OldPrimitiveGroupChunk.vertexTypeMap:
                    chunkVertexType = OldPrimitiveGroupChunk.vertexTypeMap[chunk.identifier]
                    vertexType |= chunkVertexType
        
        if uvListCount > 0:
            if uvListCount > 8:
                raise Exception("Old Primitive Groups can only have a maximum of 8 UV Lists.")
            
            vertexType |= OldPrimitiveGroupChunk.uvTypeMap[uvListCount - 1]

        return vertexType

    def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
        binaryWriter.writeUInt32(self.version)
        binaryWriter.writePure3DString(self.shaderName)
        binaryWriter.writeUInt32(self.primitiveType)
        binaryWriter.writeUInt32(self.getVertexType())
        binaryWriter.writeUInt32(self.numberOfVertices)
        binaryWriter.writeUInt32(self.numberOfIndices)
        binaryWriter.writeUInt32(self.numberOfMatrices)