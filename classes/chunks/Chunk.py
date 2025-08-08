from __future__ import annotations

from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

#
# Class
#

class Chunk():
    @staticmethod
    def parseData(data : bytes, isLittleEndian : bool = True) -> list:
        return []

    def __init__(
        self, 
        identifier : int, 
        children : list[Chunk] = None
    ) -> None:
        self.identifier = identifier

        self.children = [] if children is None else children

    def getChildrenSize(self) -> int:
        childrenSize = 0

        for child in self.children:
            childrenSize += child.getEntireSize()

        return childrenSize

    def getDataSize(self) -> int:
        binaryWriter = Pure3DBinaryWriter()

        self.writeData(binaryWriter)

        # HACK: Feels kind of hacky, idk, I feel like it should get the length of 
        #     the binaryWriter's buffer minus the extra allocated space
        #    this also feels like it may cause problems when writing files...
        return binaryWriter.getPosition()

    def getEntireSize(self) -> int:
        return 12 + self.getDataSize() + self.getChildrenSize()

    def write(self, binaryWriter : Pure3DBinaryWriter) -> None:
        binaryWriter.writeUInt32(self.identifier)

        dynamicFieldsPosition = binaryWriter.getPosition()

        binaryWriter.writeUInt32(0) # Placeholder for dataSize

        binaryWriter.writeUInt32(0) # Placeholder for entireSize

        beforeDataSize = binaryWriter.getPosition()
        self.writeData(binaryWriter)
        dataSize = binaryWriter.getPosition() - beforeDataSize

        beforeChildrenSize = binaryWriter.getPosition()
        for child in self.children:
            child.write(binaryWriter)
        childrenSize = binaryWriter.getPosition() - beforeChildrenSize
        
        continuingPosition = binaryWriter.getPosition()
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
