from __future__ import annotations

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

#
# Class
#

class Chunk():
    @staticmethod
    def parseData(binaryReader: Pure3DBinaryReader) -> list:
        return []

    def __init__(
        self, 
        identifier : int, 
        children : list[Chunk] = None
    ) -> None:
        self.identifier = identifier

        self.children = [] if children is None else children

    def write(self, binaryWriter : Pure3DBinaryWriter) -> None:
        binaryWriter.writeUInt32(self.identifier)

        dynamicFieldsPosition = binaryWriter.position

        binaryWriter.writeUInt32(0) # Placeholder for dataSize

        binaryWriter.writeUInt32(0) # Placeholder for entireSize

        beforeDataSize = binaryWriter.position
        self.writeData(binaryWriter)
        dataSize = binaryWriter.position - beforeDataSize

        beforeChildrenSize = binaryWriter.position
        for child in self.children:
            child.write(binaryWriter)
        childrenSize = binaryWriter.position - beforeChildrenSize
        
        continuingPosition = binaryWriter.position
        binaryWriter.seek(dynamicFieldsPosition)

        binaryWriter.writeUInt32(12 + dataSize)

        binaryWriter.writeUInt32(12 + dataSize + childrenSize)

        binaryWriter.seek(continuingPosition)

    def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
        pass

    def getFirstChildOfType(self, type) -> Chunk:
        for chunk in self.children:
            if isinstance(chunk, type):
                return chunk

        return None

    def getChildrenOfType(self, type) -> list[Chunk]:
        children = []

        for chunk in self.children:
            if isinstance(chunk, type):
                children.append(chunk)

        return children
