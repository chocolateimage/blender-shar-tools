from __future__ import annotations

import bpy
import mathutils

#
# Utility Functions
#

def createFence(start : mathutils.Vector, end : mathutils.Vector, normal : mathutils.Vector, name : str | None = None) -> bpy.types.Object:
    #
    # Calculate Normal
    #

    calculatedNormal = (end - start).cross(mathutils.Vector((0, 1, 0))).normalized()

    calculatedNormal.y = 0

    dot = normal.dot(calculatedNormal)

    #
    # Flip (if necessary)
    #

    isFlipped = dot < 0

    if isFlipped:
        start, end = end, start

    #
    # Name
    #

    name = name if name is not None else "Fence"

    #
    # Create Curve
    #

    # https://docs.blender.org/api/current/bpy.types.Curve.html
    fenceCurve = bpy.data.curves.new(name, "CURVE")

    fenceCurve.dimensions = "2D"

    fenceCurve.extrude = 50

    #
    # Create Spline
    #

    # https://docs.blender.org/api/current/bpy.types.CurveSplines.html
    fenceCurveSpline = fenceCurve.splines.new("POLY")

    fenceCurveSpline.points.add(1) # Only need to add one, splines start with 1 point

    # https://docs.blender.org/api/current/bpy.types.SplinePoint.html

    fenceCurveSpline.points[0].co = (start.x, start.z, start.y, 1) # Swap Z and Y because Hit & Run uses Y for the vertical axis
    fenceCurveSpline.points[1].co = (end.x, end.z, end.y, 1) # Ditto

    fenceCurveSpline.use_smooth = False

    #
    # Create Object
    #

    # https://docs.blender.org/api/current/bpy.types.Object.html
    fence = bpy.data.objects.new(name, fenceCurve)

    fence.lock_rotation = [ True, True, False ]

    fence.isFence = True
    fence.fenceProperties.isFlipped = isFlipped

    #
    # Return
    #

    return fence