from __future__ import annotations

from classes.chunks.Chunk import Chunk

from classes.Pure3DBinaryReader import Pure3DBinaryReader
from classes.Pure3DBinaryWriter import Pure3DBinaryWriter

import data.chunkIdentifiers as chunkIdentifiers

import mathutils

class SkeletonJointChunk(Chunk):
    @staticmethod
    def parseData(binaryReader: Pure3DBinaryReader) -> list:
        name = binaryReader.readPure3DString()
        parent = binaryReader.readUInt32()
        dof = binaryReader.readInt32()
        freeAxis = binaryReader.readInt32()
        primaryAxis = binaryReader.readInt32()
        secondaryAxis = binaryReader.readInt32()
        twistAxis = binaryReader.readInt32()
        restPose = binaryReader.readPure3DMatrix()
        
        return [name, parent, dof, freeAxis, primaryAxis, secondaryAxis, twistAxis, restPose]

    def __init__(
        self, 
        identifier: int = chunkIdentifiers.SKELETON_JOINT, 
        children: list[Chunk] = None,
        name: str = "",
        parent: int = 0,
        dof: int = 0,
        freeAxis: int = 0,
        primaryAxis: int = 0,
        secondaryAxis: int = 0,
        twistAxis: int = 0,
        restPose: mathutils.Matrix = None,
    ) -> None:
        super().__init__(identifier, children)
    
        self.name = name
        self.parent = parent
        self.dof = dof
        self.freeAxis = freeAxis
        self.primaryAxis = primaryAxis
        self.secondaryAxis = secondaryAxis
        self.twistAxis = twistAxis
        self.restPose = mathutils.Matrix() if restPose is None else restPose

    def writeData(self, binaryWriter : Pure3DBinaryWriter) -> None:
        binaryWriter.writePure3DString(self.name)
        binaryWriter.writeUInt32(self.parent)
        binaryWriter.writeInt32(self.dof)
        binaryWriter.writeInt32(self.freeAxis)
        binaryWriter.writeInt32(self.primaryAxis)
        binaryWriter.writeInt32(self.secondaryAxis)
        binaryWriter.writeInt32(self.twistAxis)
        binaryWriter.writePure3DMatrix(self.restPose)
