#
# Imports
#

from __future__ import annotations

import bpy
import mathutils

#
# Utility Functions
#

def createPath(points : list[mathutils.Vector], name : str | None = None) -> bpy.types.Object:
	#
	# Create Curve
	#

	pathCurve = bpy.data.curves.new("Fence", "CURVE")

	pathCurve.dimensions = "2D"

	#
	# Create Spline
	#

	pathCurveSpline = pathCurve.splines.new("POLY")

	pathCurveSpline.points.add(len(points) - 1)

	for point in range(len(points)):
		pathCurveSpline.points[point].co = (points[point].x, points[point].z, points[point].y, 1) # Swap Z and Y because Hit & Run uses Y for the vertical axis

	pathCurveSpline.use_smooth = False

	#
	# Create Object
	#

	name = name if name is not None else "Path"

	path = bpy.data.objects.new(name, pathCurve)

	path.isPath = True

	#
	# Return
	#

	return path