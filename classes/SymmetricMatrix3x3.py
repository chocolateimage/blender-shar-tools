from __future__ import annotations

import mathutils

#
# Class
#


# From https://github.com/Hampo/NetP3DLib/blob/main/NetP3DLib/NetP3DLib/Numerics/SymmetricMatrix3x3.cs



# Credits: Lucas Cardellini
class SymmetricMatrix3x3:
    @staticmethod
    def Identity():
        return SymmetricMatrix3x3(xx = 1, yy = 1, zz = 1)

    @staticmethod
    def Zero():
        return SymmetricMatrix3x3()

    # Credits: EnAppelsin
    @staticmethod
    def Outer(r: mathutils.Vector):
        return SymmetricMatrix3x3(
            xx = r.x * r.x,
            xy = r.x * r.y,
            xz = r.x * r.z,
            yy = r.y * r.y,
            yz = r.y * r.z,
            zz = r.z * r.z
        )

    # Credits: EnAppelsin
    @staticmethod
    def Translate(inertia: SymmetricMatrix3x3, centre: mathutils.Vector):
        return inertia + (SymmetricMatrix3x3.Identity() * centre.length_squared - SymmetricMatrix3x3.Outer(centre))

    def __init__(self, xx: float = 0, xy: float = 0, xz: float = 0, yy: float = 0, yz: float = 0, zz: float = 0):
        self.xx: float = xx
        self.xy: float = xy
        self.xz: float = xz
        self.yy: float = yy
        self.yz: float = yz
        self.zz: float = zz
    
    def __add__(self, other: SymmetricMatrix3x3):
        left = self
        right = other
        return SymmetricMatrix3x3(
            xx = left.xx + right.xx,
            xy = left.xy + right.xy,
            xz = left.xz + right.xz,

            yy = left.yy + right.yy,
            yz = left.yz + right.yz,

            zz = left.zz + right.zz,
        )

    def __sub__(self, other: SymmetricMatrix3x3):
        left = self
        right = other
        return SymmetricMatrix3x3(
            xx = left.xx - right.xx,
            xy = left.xy - right.xy,
            xz = left.xz - right.xz,

            yy = left.yy - right.yy,
            yz = left.yz - right.yz,

            zz = left.zz - right.zz,
        )

    def __mul__(self, other):
        if isinstance(other, SymmetricMatrix3x3):
            left = self
            right = other
            return SymmetricMatrix3x3(
                xx = (left.xx * right.xx) + (left.xy * right.xy) + (left.xz * right.xz),
                xy = (left.xx * right.xy) + (left.xy * right.yy) + (left.xz * right.yz),
                xz = (left.xx * right.xz) + (left.xy * right.yz) + (left.xz * right.zz),
                yy = (left.xy * right.xy) + (left.yy * right.yy) + (left.yz * right.yz),
                yz = (left.xy * right.xz) + (left.yy * right.yz) + (left.yz * right.zz),
                zz = (left.xz * right.xz) + (left.yz * right.yz) + (left.zz * right.zz)
            )
        elif isinstance(other, float):
            left = self
            right = other
            return SymmetricMatrix3x3(
                xx = left.xx * right,
                xy = left.xy * right,
                xz = left.xz * right,
                yy = left.yy * right,
                yz = left.yz * right,
                zz = left.zz * right
            )
        else:
            raise NotImplementedError("Cannot multiply " + type(self).__name__ + " with " + type(other).__name__)
