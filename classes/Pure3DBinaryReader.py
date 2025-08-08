from __future__ import annotations

import mathutils

from classes.BinaryReader import BinaryReader
from classes.Colour import Colour
from classes.SymmetricMatrix3x3 import SymmetricMatrix3x3

#
# Class
#

class Pure3DBinaryReader(BinaryReader):
    def readPure3DColour(self) -> Colour:
        valueBytes = self.readBytes(4)

        if not self.isLittleEndian:
            valueBytes = bytes(reversed(list(valueBytes)))

        blue = valueBytes[0]

        green = valueBytes[1]

        red = valueBytes[2]

        alpha = valueBytes[3]

        return Colour(red, green, blue, alpha)

    def readPure3DFourCharacterCode(self) -> str:
        rawString = self.readString(4)

        if not self.isLittleEndian:
            rawStringCharacters = list(rawString)

            rawStringCharacters.reverse()

            rawString = "".join(rawStringCharacters)

        return self.trimNull(rawString)

    def readPure3DMatrix(self) -> mathutils.Matrix:
        matrix : list[float] = []

        for i in range(16):
            matrix.append(self.readFloat())

        return mathutils.Matrix(
            [
                [ matrix[0], matrix[1], matrix[2], matrix[3] ],
                [ matrix[4], matrix[5], matrix[6], matrix[7] ],
                [ matrix[8], matrix[9], matrix[10], matrix[11] ],
                [ matrix[12], matrix[13], matrix[14], matrix[15] ],
            ])

    def readPure3DString(self) -> str:
        stringLength = self.readByte()

        string = self.readString(stringLength)

        return self.trimNull(string)

    def readPure3DVector2(self) -> mathutils.Vector:
        x = self.readFloat()

        y = self.readFloat()

        return mathutils.Vector((x, y))

    def readPure3DVector3(self) -> mathutils.Vector:
        x = self.readFloat()

        y = self.readFloat()

        z = self.readFloat()

        return mathutils.Vector((x, y, z))

    def readSymmetricMatrix3x3(self) -> SymmetricMatrix3x3:
        xx = self.readFloat()

        xy = self.readFloat()

        xz = self.readFloat()


        yy = self.readFloat()

        yz = self.readFloat()


        zz = self.readFloat()

        return SymmetricMatrix3x3(xx, xy, xz, yy, yz, zz)
        
    def trimNull(self, string) -> str:
        nullIndex = string.find("\0")

        if nullIndex == -1:
            return string

        return string[:nullIndex]