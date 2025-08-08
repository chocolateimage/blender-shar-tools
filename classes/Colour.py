from __future__ import annotations

import mathutils

#
# Class
#

class Colour:
    @staticmethod
    def fromFloatVector(vector: mathutils.Vector | tuple):
        if len(vector) == 3:
            return Colour(round(vector[0] * 255), round(vector[1] * 255), round(vector[2] * 255), 255)
        if len(vector) >= 4:
            return Colour(round(vector[0] * 255), round(vector[1] * 255), round(vector[2] * 255), round(vector[3] * 255))

    def __init__(self, red : int, green : int, blue : int, alpha : int) -> None:
        self.red : int = red

        self.green : int = green

        self.blue : int = blue

        self.alpha : int = alpha
    
    def __iter__(self):
        yield self.red / 255
        yield self.green / 255
        yield self.blue / 255
        yield self.alpha / 255