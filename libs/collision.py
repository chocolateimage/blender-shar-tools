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

from classes.SymmetricMatrix3x3 import SymmetricMatrix3x3

import mathutils
import math

import numpy as np

#
# Utility Functions
#

def createCollision(collisionObject: CollisionObjectChunk, collisionEffect: CollisionEffectChunk | None = None, physicsObject: PhysicsObjectChunk | None = None) -> list[bpy.types.Object]:
    collisions = createFromVolume(collisionObject,collisionObject.getFirstChildOfType(CollisionVolumeChunk))
    if len(collisions) > 0:
        if collisionEffect is not None:
            collisionProperties = collisions[0].collisionProperties
            collisionProperties.hasCollisionEffect = True
            collisionProperties.collisionEffectClassType = str(collisionEffect.classType)
            collisionProperties.collisionEffectPhyPropID = str(collisionEffect.phyPropID)
            collisionProperties.collisionEffectSound = collisionEffect.soundResourceDataName
            if physicsObject is not None:
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

# Code from https://github.com/Hampo/SHARCarPhysicsObjectGenerator/blob/main/SHARCarPhysicsObjectGenerator/SHARCarPhysicsObjectGenerator/PhysicsObjectGenerator.cs
# Converted from C# to Python using ChatGPT (i don't have the time for this)

def transpose(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    result = np.zeros((cols, rows))

    for i in range(rows):
        for j in range(cols):
            result[j, i] = matrix[i, j]

    return result

def multiply(a, b):
    a_rows = len(a)
    a_cols = len(a[0])
    b_cols = len(b[0])

    result = np.zeros((a_rows, b_cols))

    for i in range(a_rows):
        for j in range(b_cols):
            result[i, j] = sum(a[i][k] * b[k][j] for k in range(a_cols))

    return result

def calculate_centre_of_mass(volumes: list[CollisionVolumeChunk]):
    total_mass = 0.0
    weighted_sum = mathutils.Vector()

    for volume in volumes:
        if len(volume.children) == 0:
            continue
        vector = volume.children[0].getFirstChildOfType(CollisionVectorChunk)
        if vector is None:
            continue

        mass = calculate_volume_mass(volume)
        total_mass += mass
        weighted_sum += vector.vector * mass

    return weighted_sum / total_mass if total_mass > 0 else mathutils.Vector()

def calculate_volume_mass(volume: CollisionVolumeChunk):
    sphere: CollisionSphereChunk = volume.getFirstChildOfType(CollisionSphereChunk)
    if sphere:
        return (4.0 / 3.0) * math.pi * (sphere.radius ** 3)
    
    obb: CollisionOrientedBoundingBoxChunk = volume.getFirstChildOfType(CollisionOrientedBoundingBoxChunk)
    if obb is not None:
        return 8.0 * obb.halfExtents.x * obb.halfExtents.y * obb.halfExtents.z
    
    cylinder: CollisionCylinderChunk = volume.getFirstChildOfType(CollisionCylinderChunk)
    if cylinder is not None:
        if cylinder.flatEnd:
            return 2 * math.pi * (cylinder.cylinderRadius ** 2) * cylinder.length
        else:
            return 2 * math.pi * cylinder.cylinderRadius * (cylinder.length * cylinder.cylinderRadius + (2/3) * cylinder.cylinderRadius ** 2)
    
    return 0.0

def calculate_inertia_matrix(volumes: list[CollisionVolumeChunk], centre_of_mass: mathutils.Vector):
    inertia_matrix = SymmetricMatrix3x3()
    total_mass = 0.0

    for volume in volumes:
        if len(volume.children) == 0:
            continue
        vector = volume.children[0].getFirstChildOfType(CollisionVectorChunk)
        if vector is None:
            continue

        mass = calculate_volume_mass(volume)
        total_mass += mass

        obb: CollisionOrientedBoundingBoxChunk = volume.getFirstChildOfType(CollisionOrientedBoundingBoxChunk)
        sphere: CollisionSphereChunk = volume.getFirstChildOfType(CollisionSphereChunk)
        cylinder: CollisionCylinderChunk = volume.getFirstChildOfType(CollisionCylinderChunk)

        if obb is not None:
            ex, ey, ez = obb.halfExtents.x * 2, obb.halfExtents.y * 2, obb.halfExtents.z * 2
            mass_factor = 1.0 / 12.0

            inertia = np.array([
                [mass_factor * (ey**2 + ez**2), 0, 0],
                [0, mass_factor * (ex**2 + ez**2), 0],
                [0, 0, mass_factor * (ex**2 + ey**2)]
            ])

            vectors = obb.getChildrenOfType(CollisionVectorChunk)
            if len(vectors) != 4:
                raise ValueError("A Collision Oriented Bounding Box Chunk does not have the correct number of sub vectors.")

            matrix_x = vectors[1].vector
            matrix_y = vectors[2].vector
            matrix_z = vectors[3].vector

            rot = np.array([
                [matrix_x.x, matrix_x.y, matrix_x.z],
                [matrix_y.x, matrix_y.y, matrix_y.z],
                [matrix_z.x, matrix_z.y, matrix_z.z]
            ])

            rot_t = transpose(rot)
            inertia_rotated = multiply(multiply(rot_t, inertia), rot)

            local_matrix = SymmetricMatrix3x3(
                inertia_rotated[0, 0], inertia_rotated[0, 1], inertia_rotated[0, 2],
                inertia_rotated[1, 1], inertia_rotated[1, 2],
                inertia_rotated[2, 2]
            )

            centre = vectors[0].vector - centre_of_mass
            local_matrix_translated = SymmetricMatrix3x3.Translate(local_matrix, centre)

            inertia_matrix += local_matrix_translated

        elif sphere is not None:
            radius = sphere.radius
            mass_factor = 2.0 / 5.0

            inertia_value = mass_factor * radius * radius
            vectors = sphere.getChildrenOfType(CollisionVectorChunk)
            if len(vectors) != 1:
                raise ValueError("A Collision Sphere Chunk does not have the correct number of sub vectors.")

            local_matrix = SymmetricMatrix3x3(inertia_value, 0, 0, inertia_value, 0, inertia_value)

            centre = vectors[0].vector - centre_of_mass
            local_matrix_translated = SymmetricMatrix3x3.Translate(local_matrix, centre)

            inertia_matrix += local_matrix_translated

        elif cylinder is not None:
            childChunks = cylinder.getChildrenOfType(CollisionVectorChunk)
            center: mathutils.Vector  = childChunks[0].vector
            axis: mathutils.Vector  = childChunks[1].vector

            m = SymmetricMatrix3x3.Identity()

            if cylinder.flatEnd:
                h = 2.0 * cylinder.length
            else:
                h = 2.0 * (cylinder.length + cylinder.cylinderRadius * 2.0 / 3.0)

            r2 = cylinder.cylinderRadius ** 2
            h2 = h ** 2
            m.xx = r2 / 2.0
            m.yy = m.zz = (h2 + 3.0 * r2) / 12.0

            x = mathutils.Vector((1.0, 0.0, 0.0))
            O2 = x.cross(axis)

            if O2.length < 0.001:
                continue

            O2.normalize()
            O3 = axis.cross(O2)
            O3.normalize()

            inertia_matrix += SymmetricMatrix3x3.Translate(m, center)

        else:
            raise ValueError("Unexpected chunk type encountered.")

    return inertia_matrix * total_mass

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
                volumes = collisionObject.getFirstChildOfType(CollisionVolumeChunk).children
                centreOfMass = calculate_centre_of_mass(volumes)
                matrix = calculate_inertia_matrix(volumes, centreOfMass)
                physicsObject = PhysicsObjectChunk(
                    name = name,
                    numJoints = 0,
                    version = 1,
                    volume = i.collisionProperties.physicsVolume,
                    restingSensitivity = i.collisionProperties.physicsRestingSensitivity,
                    children = [
                        PhysicsVectorChunk(vector = centreOfMass),
                        PhysicsInertiaMatrixChunk(matrix = matrix)
                    ]
                )


    chunks = [
        collisionObject,
        collisionEffect
    ]
    if physicsObject is not None:
        chunks.insert(0,physicsObject)
    return chunks

def collisionsToCollisionObject(name: str, collisions: list[bpy.types.Object]):
    volume = CollisionVolumeChunk(
        ownerIndex = 0,
    )

    volume.children.append(CollisionAxisAlignedBoundingBoxChunk())
    
    for collision in collisions:
        if collision.collisionProperties is None:
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