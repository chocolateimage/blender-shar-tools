import mathutils
import math
from dataclasses import dataclass

from classes.chunks.IntersectChunk import IntersectChunk
from classes.chunks.SurfaceTypeListChunk import SurfaceTypeListChunk
from classes.chunks.BoundingBoxChunk import BoundingBoxChunk
from classes.chunks.BoundingSphereChunk import BoundingSphereChunk

import bpy
import bmesh

GROUP_SIZE = 20
INTERSECT_DEBUG = False

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

def convertToChunks(faces: list[Face]):
    if len(faces) == 0:
        return []
    bm = bmesh.new()
    
    x_from = math.inf
    x_to = -math.inf

    z_from = math.inf
    z_to = -math.inf

    for i in faces:
        verts = []
        for vertex in i.vertices:
            if vertex.x < x_from:
                x_from = vertex.x
            if vertex.z < z_from:
                z_from = vertex.z

            if vertex.x > x_to:
                x_to = vertex.x
            if vertex.z > z_to:
                z_to = vertex.z
            verts.append(bm.verts.new(vertex))
        bmface: bmesh.types.BMFace = bm.faces.new(verts)
        bmface.material_index = i.terrainType
    
    # Align from/to for range to 20ers
    x_from = int(x_from / GROUP_SIZE) * GROUP_SIZE - GROUP_SIZE
    x_to = int(x_to / GROUP_SIZE) * GROUP_SIZE + GROUP_SIZE

    z_from = int(z_from / GROUP_SIZE) * GROUP_SIZE - GROUP_SIZE
    z_to = int(z_to / GROUP_SIZE) * GROUP_SIZE + GROUP_SIZE

    # https://blender.stackexchange.com/a/3629
    for i in range(x_from, x_to, GROUP_SIZE):
        ret = bmesh.ops.bisect_plane(bm, geom=bm.verts[:]+bm.edges[:]+bm.faces[:], plane_co=(i,0,0), plane_no=(-1,0,0))
        bmesh.ops.split_edges(bm, edges=[e for e in ret["geom_cut"] if isinstance(e, bmesh.types.BMEdge)])

    for i in range(z_from, z_to, GROUP_SIZE):
        ret = bmesh.ops.bisect_plane(bm, geom=bm.verts[:]+bm.edges[:]+bm.faces[:], plane_co=(0,0,i), plane_no=(0,0,1))
        bmesh.ops.split_edges(bm, edges=[e for e in ret["geom_cut"] if isinstance(e, bmesh.types.BMEdge)])

    bmesh.ops.triangulate(bm, faces=bm.faces[:])

    groups = {}

    for face in bm.faces:
        center = face.calc_center_median()
        groupid = ",".join([
            str(math.floor(i / GROUP_SIZE))
            for
            i
            in
            [center.x,center.z]
        ])
        if groupid not in groups:
            groups[groupid] = [face]
        else:
            groups[groupid].append(face)

    chunks = []
    for group in groups.values():
        indices = []
        positions = []
        normals = []
        surfaceTypes = []
        boundingBoxMin = mathutils.Vector((99999,99999,99999))
        boundingBoxMax = mathutils.Vector((-99999,-99999,-99999))

        for face in group:
            face: bmesh.types.BMFace
            for i in face.verts:
                co = i.co.xyz
                positions.append(co)
                indices.append(len(positions) - 1)

                if co.x < boundingBoxMin.x:
                    boundingBoxMin.x = co.x
                if co.y < boundingBoxMin.y:
                    boundingBoxMin.y = co.y
                if co.z < boundingBoxMin.z:
                    boundingBoxMin.z = co.z

                if co.x > boundingBoxMax.x:
                    boundingBoxMax.x = co.x
                if co.y > boundingBoxMax.y:
                    boundingBoxMax.y = co.y
                if co.z > boundingBoxMax.z:
                    boundingBoxMax.z = co.z

            normal = face.normal.xyz
            if normal.y < 0:
                normal.y = -normal.y
            normals.append(normal)

            surfaceTypes.append(face.material_index)
        
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
    
    if INTERSECT_DEBUG:
        ivm = bpy.data.meshes.new("IntersectVisualizationMesh")
        bm.to_mesh(ivm)

        ivo = bpy.data.objects.new("IntersectVisualizationObject",ivm)
        bpy.context.scene.collection.objects.link(ivo)

    bm.free()

    return chunks