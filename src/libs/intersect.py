import mathutils
import math
from dataclasses import dataclass

from classes.chunks.IntersectChunk import IntersectChunk
from classes.chunks.SurfaceTypeListChunk import SurfaceTypeListChunk
from classes.chunks.BoundingBoxChunk import BoundingBoxChunk
from classes.chunks.BoundingSphereChunk import BoundingSphereChunk

import random

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

	def size(self):
		center = self.center()
		distance = 0
		for i in self.vertices:
			vertex_distance = (i - center).length
			if vertex_distance > distance:
				distance = vertex_distance
		return distance

	def groupLocation(self):
		center = self.center()
		x = math.floor(center.x / GROUP_SIZE)
		y = math.floor(center.z / GROUP_SIZE)
		return (x,y)

	def groupId(self):
		x, y = self.groupLocation()
		return f"{x},{y}"

	def clampToGroup(self):
		x, y = self.groupLocation()
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

	def doesFit(self):
		x, y = self.groupLocation()
		xmin = x * GROUP_SIZE
		ymin = y * GROUP_SIZE
		xmax = (x+1) * GROUP_SIZE
		ymax = (y+1) * GROUP_SIZE
		for i in self.vertices:
			if i.x < xmin or i.x > xmax:
				return False
			if i.z < ymin or i.z > ymax:
				return False
		return True


	def splitOnce(self):
		side_a = [
			self.vertices[2],
			self.vertices[1],
			(self.vertices[0] + self.vertices[1]) / 2,
		]
		side_b = [
			self.vertices[2],
			self.vertices[0],
			(self.vertices[0] + self.vertices[1]) / 2,
		]
		return [
			Face(
				vertices=side_a,
				terrainType=self.terrainType
			),
			Face(
				vertices=side_b,
				terrainType=self.terrainType
			)
		]
	
	def splitUntilFits(self,recursion=0):
		if recursion > 1000:
			print("[Face.splitUntilFits] Escaped recursion!",self)
			return [self.clampToGroup()]
		faces = []
		if self.doesFit():
			faces.append(self)
		else:
			if self.size() < 0.1:
				return [self.clampToGroup()]
			for face in self.splitOnce():
				faces.extend(face.splitUntilFits(recursion+1))

		return faces

@dataclass
class Group():
	faces: list[Face]

def convertToChunks(l: list[Face]):
	chunks = []
	groups = {}
	for i in l:
		for face in i.splitUntilFits():
			groupid = face.groupId()
			if groupid not in groups:
				groups[groupid] = Group(faces=[])
			groups[groupid].faces.append(face)
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