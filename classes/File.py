from __future__ import annotations

from classes.chunks.Chunk import Chunk
from classes.chunks.RootChunk import RootChunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

from instances.defaultChunkRegistry import defaultChunkRegistry

#
# Class
#

class File:
    class Signatures:
        LITTLE_ENDIAN = 0xFF443350 # P3Dÿ

        LITTLE_ENDIAN_COMPRESSED = 0x5A443350 # P3DZ

        BIG_ENDIAN = 0x503344FF # ÿD3P

        BIG_ENDIAN_COMPRESSED = 0x5033445A # ZD3P

    @staticmethod
    def fromBytes(buffer: bytes) -> RootChunk:
        #
        # Read Buffer
        #

        binaryReader = Pure3DBinaryReader(buffer, True)

        fileIdentifier = binaryReader.readUInt32()

        #
        # Decompress File (if needed)
        #

        # TODO

        #
        # Handle Endianness
        #

        if fileIdentifier == File.Signatures.LITTLE_ENDIAN:
            pass
        elif fileIdentifier == File.Signatures.BIG_ENDIAN:
            binaryReader.isLittleEndian = False
        else:
            raise Exception("Input bytes are not a P3D file.")
        
        binaryReader.seekOffset(8)

        #
        # Create Root Chunk
        #

        chunk = RootChunk(identifier = fileIdentifier, children = File._readChunkChildren(binaryReader))
        return chunk

    @staticmethod
    def toBytes(chunks : list[Chunk], littleEndian : bool = True) -> bytes:
        binaryWriter = Pure3DBinaryWriter(littleEndian)
        
        # Note: Even when writing a big-endian file, the file signature here should still be little-endian.
        #    It will be converted to big-endian when the file is written.
        binaryWriter.writeUInt32(File.Signatures.LITTLE_ENDIAN)

        binaryWriter.writeUInt32(12)

        chunkSizePosition = binaryWriter.getPosition()
        binaryWriter.writeUInt32(0) # Placeholder for chunk size

        lastPositionWritingChunks = binaryWriter.getPosition()

        for chunk in chunks:
            chunk.write(binaryWriter)
        
        chunksSize = binaryWriter.getPosition() - lastPositionWritingChunks

        binaryWriter.seek(chunkSizePosition)
        binaryWriter.writeUInt32(12 + chunksSize)
        binaryWriter.seek(lastPositionWritingChunks + chunksSize)

        return binaryWriter.getBytes()

    @staticmethod
    def _readChunk(binaryReader: Pure3DBinaryReader) -> tuple[Chunk, int]:
        #
        # Get Chunk Header Data
        #

        identifier = binaryReader.readUInt32()

        dataSize = binaryReader.readUInt32()

        entireSize = binaryReader.readUInt32()

        #
        # Get Chunk Class
        #

        chunkClass = defaultChunkRegistry.getClass(identifier)

        #
        # Get Data
        #

        parsedData = []

        if dataSize > 12:
            extraDataSize = dataSize - 12

            originalPosition = binaryReader.getPosition()
            parsedData = chunkClass.parseData(binaryReader)
            binaryReader.seek(originalPosition + extraDataSize)

        #
        # Get Children
        #

        children : list[Chunk] = []

        if entireSize > dataSize:
            childrenDataSize = entireSize - dataSize

            children = File._readChunkChildren(binaryReader, binaryReader.getPosition() + childrenDataSize)

        #
        # Return
        #

        # Note: We now return the entireSize here because chocolateimage
        #    found this to me notably faster in _readChunkChildren than
        #    calling getEntireSize (which "writes" all the data to get the size)
        return chunkClass(identifier, children, *parsedData)

    @staticmethod
    def _readChunkChildren(binaryReader: Pure3DBinaryReader, endBufferOffset: int | None = None) -> list[Chunk]:
        children : list[Chunk] = []

        endBufferOffset = endBufferOffset if endBufferOffset is not None else binaryReader.getLength()

        while binaryReader.getPosition() < endBufferOffset:
            chunk = File._readChunk(binaryReader)

            children.append(chunk)

        return children