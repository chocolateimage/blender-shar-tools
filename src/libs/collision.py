#
# Imports
#

import bpy
import bmesh

from classes.chunks.CollisionObjectChunk import CollisionObjectChunk
from classes.chunks.CollisionVolumeChunk import CollisionVolumeChunk
from classes.chunks.CollisionOrientedBoundingBoxChunk import CollisionOrientedBoundingBoxChunk
from classes.chunks.CollisionVectorChunk import CollisionVectorChunk
from classes.chunks.CollisionCylinderChunk import CollisionCylinderChunk
from classes.chunks.CollisionSphereChunk import CollisionSphereChunk
from classes.chunks.CollisionObjectAttributeChunk import CollisionObjectAttributeChunk
from classes.chunks.CollisionAxisAlignedBoundingBoxChunk import CollisionAxisAlignedBoundingBoxChunk
from classes.chunks.CollisionEffectChunk import CollisionEffectChunk
from classes.chunks.PhysicsObjectChunk import PhysicsObjectChunk
from classes.chunks.PhysicsVectorChunk import PhysicsVectorChunk
from classes.chunks.PhysicsInertiaMatrixChunk import PhysicsInertiaMatrixChunk

import mathutils
import math

#
# Utility Functions
#

def createCollision(collisionObject: CollisionObjectChunk, collisionEffect: CollisionEffectChunk | None = None, physicsObject: PhysicsObjectChunk | None = None) -> list[bpy.types.Object]:
	collisions = createFromVolume(collisionObject,collisionObject.getFirstChildOfType(CollisionVolumeChunk))
	if len(collisions) > 0:
		if collisionEffect != None:
			collisionProperties = collisions[0].collisionProperties
			collisionProperties.hasCollisionEffect = True
			collisionProperties.collisionEffectClassType = str(collisionEffect.classType)
			collisionProperties.collisionEffectPhyPropID = str(collisionEffect.phyPropID)
			collisionProperties.collisionEffectSound = collisionEffect.soundResourceDataName
			if physicsObject != None:
				collisionProperties.physicsRestingSensitivity = physicsObject.restingSensitivity
				collisionProperties.physicsVolume = physicsObject.volume
	return collisions

def createNewCollisionBox():
	mesh = bpy.data.meshes.new("Collision Box")
	obj = bpy.data.objects.new("Collision Box", mesh)

	bm = bmesh.new()
	bmesh.ops.create_cube(bm, size=2)
	bm.to_mesh(mesh)
	bm.free()

	obj.collisionProperties.collisionType = "Box"
	return obj

def createNewCollisionCylinder(radius: float, length: float, flatEnd: bool):
	mesh = bpy.data.meshes.new("Collision Cylinder")
	obj = bpy.data.objects.new("Collision Cylinder", mesh)

	bm = bmesh.new()
	bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=1)
	bm.to_mesh(mesh)
	bm.free()

	combinedstring = ""
	for i in obj.data.vertices:
		combinedstring += str(i.co.x) + ","
		combinedstring += str(i.co.y) + ","
		combinedstring += str(i.co.z)
		combinedstring += "|"
	obj.collisionProperties.originalCoords = combinedstring

	obj.collisionProperties.collisionType = "Cylinder"
	obj.collisionProperties.radius = radius
	obj.collisionProperties.length = length
	obj.collisionProperties.flatEnd = flatEnd
	return obj

def createNewCollisionSphere(radius: float):
	mesh = bpy.data.meshes.new("Collision Sphere")
	obj = bpy.data.objects.new("Collision Sphere", mesh)

	bm = bmesh.new()
	bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=1)
	bm.to_mesh(mesh)
	bm.free()

	combinedstring = ""
	for i in obj.data.vertices:
		combinedstring += str(i.co.x) + ","
		combinedstring += str(i.co.y) + ","
		combinedstring += str(i.co.z)
		combinedstring += "|"
	obj.collisionProperties.originalCoords = combinedstring

	obj.collisionProperties.collisionType = "Sphere"
	obj.collisionProperties.radius = radius

	return obj

def createFromVolume(collisionObject: CollisionObjectChunk, collisionVolume: CollisionVolumeChunk) -> list[bpy.types.Object]:
	objects = []

	for child in collisionVolume.children:
		if isinstance(child, CollisionVolumeChunk):
			objects.extend(createFromVolume(collisionObject,child))
		elif isinstance(child, CollisionOrientedBoundingBoxChunk):
			centerChunk, rotationMatrixXChunk, rotationMatrixYChunk, rotationMatrixZChunk = child.getChildrenOfType(CollisionVectorChunk)
			matrix = mathutils.Matrix((
				(rotationMatrixXChunk.vector.x,rotationMatrixYChunk.vector.x,rotationMatrixZChunk.vector.x,),
				(rotationMatrixXChunk.vector.y,rotationMatrixYChunk.vector.y,rotationMatrixZChunk.vector.y,),
				(rotationMatrixXChunk.vector.z,rotationMatrixYChunk.vector.z,rotationMatrixZChunk.vector.z,),
			))

			matrix2 = mathutils.Matrix.LocRotScale(centerChunk.vector,matrix,child.halfExtents)


			obj = createNewCollisionBox()
			for collection in obj.users_collection:
				collection.objects.unlink(obj)

			obj.name = collisionObject.name

			obj.matrix_world = matrix2
			obj.location = obj.location.xzy
			obj.rotation_euler = (mathutils.Matrix.Rotation(math.radians(90),3,"X") @ obj.rotation_euler.to_matrix()).to_euler()
			obj.rotation_euler = (mathutils.Matrix.Rotation(math.radians(180),3,"Y") @ obj.rotation_euler.to_matrix()).to_euler()

			objects.append(obj)
		elif isinstance(child, CollisionCylinderChunk):
			centerChunk, directionChunk = child.getChildrenOfType(CollisionVectorChunk)

			obj = createNewCollisionCylinder(child.cylinderRadius,child.length,child.flatEnd == 1)

			for collection in obj.users_collection:
				collection.objects.unlink(obj)

			obj.name = collisionObject.name

			z_axis = mathutils.Vector((0,0,1))
			obj.matrix_world = mathutils.Matrix.Rotation(
				z_axis.angle(directionChunk.vector),
				4,
				z_axis.cross(directionChunk.vector),
			) @ obj.matrix_world
			obj.location = centerChunk.vector.xzy

			obj.rotation_euler = (mathutils.Matrix.Rotation(math.radians(90),3,"X") @ obj.rotation_euler.to_matrix()).to_euler()
			obj.rotation_euler = (mathutils.Matrix.Rotation(math.radians(180),3,"Y") @ obj.rotation_euler.to_matrix()).to_euler()


			objects.append(obj)
		elif isinstance(child, CollisionSphereChunk):
			centerChunk = child.getFirstChildOfType(CollisionVectorChunk)
			
			obj = createNewCollisionSphere(child.radius)
			for collection in obj.users_collection:
				collection.objects.unlink(obj)

			obj.name = collisionObject.name

			obj.location = centerChunk.vector.xzy

			objects.append(obj)
		elif isinstance(child, CollisionAxisAlignedBoundingBoxChunk):
			pass
		else:
			print("Unknown collision type " + hex(child.identifier))
	
	return objects

def collisionsToChunks(name: str, collisions: list[bpy.types.Object]):
	collisionObject = collisionsToCollisionObject(name, collisions)
	collisionEffect = CollisionEffectChunk(
		classType = 7,
		phyPropID = 0,
		soundResourceDataName = "nosound"
	)
	physicsObject = None

	for i in collisions:
		if i.collisionProperties and i.collisionProperties.collisionType != "" and i.collisionProperties.hasCollisionEffect:
			collisionEffect.classType = int(i.collisionProperties.collisionEffectClassType)
			collisionEffect.phyPropID = int(i.collisionProperties.collisionEffectPhyPropID)
			collisionEffect.soundResourceDataName = i.collisionProperties.collisionEffectSound

			if collisionEffect.classType in [3, 4, 10]:
				physicsObject = PhysicsObjectChunk(
					name = name,
					numJoints = 0,
					version = 1,
					volume = i.collisionProperties.physicsVolume,
					restingSensitivity = i.collisionProperties.physicsRestingSensitivity,
					children = [
						PhysicsVectorChunk(),
						PhysicsInertiaMatrixChunk()
					]
				)


	chunks = [
		collisionObject,
		collisionEffect
	]
	if physicsObject != None:
		chunks.insert(0,physicsObject)
	return chunks

def collisionsToCollisionObject(name: str, collisions: list[bpy.types.Object]):
	volume = CollisionVolumeChunk(
		ownerIndex = 0,
	)

	volume.children.append(CollisionAxisAlignedBoundingBoxChunk())
	
	for collision in collisions:
		if collision.collisionProperties == None:
			continue
		
		properties = collision.collisionProperties
		if properties.collisionType == "Box":
			col = CollisionOrientedBoundingBoxChunk()
			col.halfExtents = collision.scale
			col.children.append(CollisionVectorChunk(vector = collision.location.xzy))
			rotation = collision.rotation_euler.to_matrix()
			rotation = mathutils.Matrix.Rotation(math.radians(180),3,"Y") @ rotation
			rotation = mathutils.Matrix.Rotation(math.radians(-90),3,"X") @ rotation
			col.children.append(CollisionVectorChunk(vector = mathutils.Vector((
				rotation[0][0],
				rotation[1][0],
				rotation[2][0],
			))))
			col.children.append(CollisionVectorChunk(vector = mathutils.Vector((
				rotation[0][1],
				rotation[1][1],
				rotation[2][1],
			))))
			col.children.append(CollisionVectorChunk(vector = mathutils.Vector((
				rotation[0][2],
				rotation[1][2],
				rotation[2][2],
			))))
			volume.children.append(CollisionVolumeChunk(children=[col],ownerIndex=-1))
		elif properties.collisionType == "Cylinder":
			col = CollisionCylinderChunk()
			col.cylinderRadius = properties.radius
			col.length = properties.length
			col.flatEnd = int(properties.flatEnd)
			col.children.append(CollisionVectorChunk(vector = collision.location.xzy))
			rotation = collision.rotation_euler.to_matrix()
			rotation = mathutils.Matrix.Rotation(math.radians(180),3,"Y") @ rotation
			rotation = mathutils.Matrix.Rotation(math.radians(-90),3,"X") @ rotation

			direction = rotation.normalized().transposed()
			directionVector = mathutils.Vector((0, 0, 1)) @ direction

			col.children.append(CollisionVectorChunk(vector = directionVector))

			volume.children.append(CollisionVolumeChunk(children=[col],ownerIndex=-1))
		elif properties.collisionType == "Sphere":
			col = CollisionSphereChunk()
			col.radius = properties.radius
			col.children.append(CollisionVectorChunk(vector = collision.location.xzy))
			volume.children.append(CollisionVolumeChunk(children=[col],ownerIndex=-1))

		

	return CollisionObjectChunk(
		children = [
			volume,
			CollisionObjectAttributeChunk()
		],
		name = name,
		version = 1,
		materialName = "NoData",
	)