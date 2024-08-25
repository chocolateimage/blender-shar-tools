import mathutils
import math
from dataclasses import dataclass

from classes.chunks.IntersectChunk import IntersectChunk
from classes.chunks.SurfaceTypeListChunk import SurfaceTypeListChunk
from classes.chunks.BoundingBoxChunk import BoundingBoxChunk
from classes.chunks.BoundingSphereChunk import BoundingSphereChunk

GROUP_SIZE = 20

def clamp(v,min,max):
	if v < min:
		return min
	if v > max:
		return max
	return v

@dataclass
class Face():
	vertices: list[mathutils.Vector]
	terrainType: int

	def center(self) -> mathutils.Vector:
		v = mathutils.Vector()
		for i in self.vertices:
			v = v + i
		return v / len(self.vertices)

	def groupLocation(self):
		center = self.center()
		x = math.floor(center.x / GROUP_SIZE)
		y = math.floor(center.z / GROUP_SIZE)
		return (x,y)

	def groupId(self):
		x, y = self.groupLocation()
		return f"{x},{y}"

	def clampTo(self,x,y):
		xmin = x * GROUP_SIZE
		ymin = y * GROUP_SIZE
		xmax = (x+1) * GROUP_SIZE
		ymax = (y+1) * GROUP_SIZE
		vertices = []
		for i in self.vertices:
			vertices.append(mathutils.Vector((
				clamp(i.x,xmin,xmax),
				i.y,
				clamp(i.z,ymin,ymax),
			)))
		return Face(vertices,self.terrainType)

@dataclass
class Group():
	faces: list[Face]

def convertToChunks(l: list[Face]):
	chunks = []
	groups = {}
	for i in l:
		print(i.center())
		groupid = i.groupId()
		if groupid not in groups:
			groups[groupid] = Group(faces=[])
		groups[groupid].faces.append(i.clampTo(*i.groupLocation()))
	print(list(groups.keys()))
	for group in groups.values():
		indices = []
		positions = []
		normals = []
		surfaceTypes = []
		boundingBoxMin = mathutils.Vector((99999,99999,99999))
		boundingBoxMax = mathutils.Vector((-99999,-99999,-99999))

		for face in group.faces:
			face: Face
			for i in face.vertices:
				positions.append(i)
				indices.append(len(positions) - 1)

				if i.x < boundingBoxMin.x:
					boundingBoxMin.x = i.x
				if i.y < boundingBoxMin.y:
					boundingBoxMin.y = i.y
				if i.z < boundingBoxMin.z:
					boundingBoxMin.z = i.z

				if i.x > boundingBoxMax.x:
					boundingBoxMax.x = i.x
				if i.y > boundingBoxMax.y:
					boundingBoxMax.y = i.y
				if i.z > boundingBoxMax.z:
					boundingBoxMax.z = i.z

			a = face.vertices[0]
			b = face.vertices[1]
			c = face.vertices[2]
			normal = ((b-a).cross(c-a)).normalized()
			normals.append(mathutils.Vector((0,1,0)) if normal.length == 0 else normal)

			surfaceTypes.append(face.terrainType)
		
		center = (boundingBoxMax + boundingBoxMin) / 2
		radius = 0
		for i in positions:
			distance = (i - center).length
			if distance > radius:
				radius = distance

		chunk = IntersectChunk(
			indices=indices,
			positions=positions,
			normals=normals,
			children=[
				SurfaceTypeListChunk(types=surfaceTypes),
				BoundingBoxChunk(
					low=boundingBoxMin,
					high=boundingBoxMax
				),
				BoundingSphereChunk(
					center=center,
					radius=radius
				)
			]
		)
		chunks.append(chunk)
	return chunks