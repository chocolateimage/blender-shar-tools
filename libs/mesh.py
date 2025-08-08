import bpy
import bmesh

import utils

import classes.chunks.IndexListChunk
import classes.chunks.MeshChunk
import classes.chunks.OldPrimitiveGroupChunk
import classes.chunks.PositionListChunk
import classes.chunks.UVListChunk
import classes.chunks.ColourListChunk
import classes.chunks.BoundingBoxChunk
import classes.chunks.BoundingSphereChunk
import classes.chunks.RenderStatusChunk

from classes.Colour import Colour

import mathutils

#
# Utility Functions
#

def createMesh(chunk: classes.chunks.MeshChunk.MeshChunk) -> bpy.types.Mesh:
    mesh = bpy.data.meshes.new(chunk.name)

    total_positions = []
    total_indices = []
    total_uvs = []
    total_colours = []

    indexoffset = 0
    separators = [0]
    for childChunkIndex, childChunk in enumerate(chunk.children):
        amount_of_positions = 0
        if isinstance(childChunk, classes.chunks.OldPrimitiveGroupChunk.OldPrimitiveGroupChunk):
            if childChunk.shaderName in bpy.data.materials:
                mesh.materials.append(bpy.data.materials[childChunk.shaderName])

            for childChildChunkIndex, childChildChunk in enumerate(childChunk.children):

                if isinstance(childChildChunk,classes.chunks.PositionListChunk.PositionListChunk):
                    for position in childChildChunk.positions:
                        total_positions.append((position.x,position.z,position.y))
                        amount_of_positions += 1
                elif isinstance(childChildChunk,classes.chunks.IndexListChunk.IndexListChunk):
                    if childChunk.primitiveType == childChunk.primitiveTypes["TRIANGLE_LIST"]:
                        for i in range(0,len(childChildChunk.indices),3):
                            tri = childChildChunk.indices[i:i+3]
                            if len(tri) < 3:
                                continue
                            total_indices.append((tri[0]+indexoffset,tri[2]+indexoffset,tri[1]+indexoffset))
                    elif childChunk.primitiveType == childChunk.primitiveTypes["TRIANGLE_STRIP"]:
                        for i in range(len(childChildChunk.indices) - 2):
                            if i % 2 == 1: # need to switch these around for some reason
                                total_indices.append((
                                    childChildChunk.indices[i] + indexoffset,
                                    childChildChunk.indices[i+1] + indexoffset,
                                    childChildChunk.indices[i+2] + indexoffset
                                ))
                            else:
                                total_indices.append((
                                    childChildChunk.indices[i] + indexoffset,
                                    childChildChunk.indices[i+2] + indexoffset,
                                    childChildChunk.indices[i+1] + indexoffset
                                ))
                    else:
                        # TODO: Implement LINE_LIST and LINE_STRIP
                        if childChunk.primitiveType == childChunk.primitiveTypes["LINE_LIST"]:
                            raise NotImplementedError("Primitive type LINE_LIST not implemented")
                        elif childChunk.primitiveType == childChunk.primitiveTypes["LINE_STRIP"]:
                            raise NotImplementedError("Primitive type LINE_STRIP not implemented")
                        else:
                            raise NotImplementedError("Primitive type "+str(childChunk.primitiveType)+" not implemented")

                elif isinstance(childChildChunk,classes.chunks.UVListChunk.UVListChunk):
                    for uv in childChildChunk.uvs:
                        total_uvs.append((uv.x,uv.y))

                elif isinstance(childChildChunk,classes.chunks.ColourListChunk.ColourListChunk):
                    for colour in childChildChunk.colours:
                        total_colours.append(colour)

        indexoffset += amount_of_positions
        separators.append(len(total_indices))

    mesh.from_pydata(total_positions,[],total_indices)
    mesh.update()
    
    uvLayer = mesh.uv_layers.new()
    vertexColor = mesh.color_attributes.new("Vertex Color", "FLOAT_COLOR", "POINT")

    for i,poly in enumerate(mesh.polygons):
        for k,j in enumerate(separators):
            if i >= j:
                poly.material_index = k
                continue
        for loop_index in poly.loop_indices:
            loop = mesh.loops[loop_index]
            vertex_index = loop.vertex_index
            uv = total_uvs[vertex_index]
            uvLayer.data[loop_index].uv = uv
            if vertex_index < len(total_colours):
                vertexColor.data[vertex_index].color = tuple(total_colours[vertex_index])
            else:
                vertexColor.data[vertex_index].color = (1,1,1,1)
    
    
    mesh.update()

    return mesh

def meshToChunk(mesh: bpy.types.Mesh, obj: bpy.types.Object) -> classes.chunks.MeshChunk.MeshChunk:
    bm = bmesh.new()
    bm.from_mesh(mesh)

    bmesh.ops.triangulate(bm, faces=bm.faces[:])

    bm.verts.ensure_lookup_table()
    bm.edges.ensure_lookup_table()
    bm.faces.ensure_lookup_table()

    meshChildren = []
    meshName = utils.get_basename(mesh.name)

    oldPrimitiveGroups: list[classes.chunks.OldPrimitiveGroupChunk.OldPrimitiveGroupChunk] = []

    if len(mesh.materials) == 0:
        oldPrimitiveGroup = classes.chunks.OldPrimitiveGroupChunk.OldPrimitiveGroupChunk(
            children=[
                #classes.chunks.VertexShaderChunk.VertexShaderChunk(), # seems to only be used on Xbox
                classes.chunks.PositionListChunk.PositionListChunk(),
                classes.chunks.UVListChunk.UVListChunk(),
                classes.chunks.ColourListChunk.ColourListChunk(),
                classes.chunks.IndexListChunk.IndexListChunk(),
            ],
            primitiveType=classes.chunks.OldPrimitiveGroupChunk.OldPrimitiveGroupChunk.primitiveTypes["TRIANGLE_LIST"]
        )
        oldPrimitiveGroups.append(oldPrimitiveGroup)
        meshChildren.append(oldPrimitiveGroup)

    for mat in mesh.materials:
        oldPrimitiveGroup = classes.chunks.OldPrimitiveGroupChunk.OldPrimitiveGroupChunk(
            children=[
                #classes.chunks.VertexShaderChunk.VertexShaderChunk(), # seems to only be used on Xbox
                classes.chunks.PositionListChunk.PositionListChunk(),
                classes.chunks.UVListChunk.UVListChunk(),
                classes.chunks.ColourListChunk.ColourListChunk(),
                classes.chunks.IndexListChunk.IndexListChunk(),
            ],
            shaderName=mat.name,
            primitiveType=classes.chunks.OldPrimitiveGroupChunk.OldPrimitiveGroupChunk.primitiveTypes["TRIANGLE_LIST"]
        )
        oldPrimitiveGroups.append(oldPrimitiveGroup)
        meshChildren.append(oldPrimitiveGroup)

    boundingBoxMin = mathutils.Vector((99999,99999,99999))
    boundingBoxMax = mathutils.Vector((-99999,-99999,-99999))

    for vertex in mesh.vertices:
        if vertex.co.x < boundingBoxMin.x:
            boundingBoxMin.x = vertex.co.x
        if vertex.co.y < boundingBoxMin.y:
            boundingBoxMin.y = vertex.co.y
        if vertex.co.z < boundingBoxMin.z:
            boundingBoxMin.z = vertex.co.z

        if vertex.co.x > boundingBoxMax.x:
            boundingBoxMax.x = vertex.co.x
        if vertex.co.y > boundingBoxMax.y:
            boundingBoxMax.y = vertex.co.y
        if vertex.co.z > boundingBoxMax.z:
            boundingBoxMax.z = vertex.co.z
    
    center = (boundingBoxMax + boundingBoxMin) / 2
    radius = 0
    for vertex in mesh.vertices:
        distance = (vertex.co - center).length
        if distance > radius:
            radius = distance

    uv_layer = bm.loops.layers.uv.active

    color_layer_verts = bm.verts.layers.color.active or bm.verts.layers.float_color.active
    color_layer_loops = bm.loops.layers.color.active or bm.loops.layers.float_color.active

    for face in bm.faces:
        oldPrimitiveGroup = oldPrimitiveGroups[face.material_index]
        indexList: classes.chunks.IndexListChunk.IndexListChunk = oldPrimitiveGroup.getFirstChildOfType(classes.chunks.IndexListChunk.IndexListChunk)
        colourList: classes.chunks.ColourListChunk.ColourListChunk = oldPrimitiveGroup.getFirstChildOfType(classes.chunks.ColourListChunk.ColourListChunk)
        positionList: classes.chunks.PositionListChunk.PositionListChunk = oldPrimitiveGroup.getFirstChildOfType(classes.chunks.PositionListChunk.PositionListChunk)
        uvList: classes.chunks.UVListChunk.UVListChunk = oldPrimitiveGroup.getFirstChildOfType(classes.chunks.UVListChunk.UVListChunk)
        
        for i in [0,2,1]:
            loop = face.loops[i]
            positionList.positions.append(loop.vert.co.xzy)
            uvList.uvs.append(loop[uv_layer].uv.xy)

            oldPrimitiveGroup.numberOfVertices += 1

            indexList.indices.append(len(positionList.positions) - 1)

            if color_layer_verts is not None:
                color = loop.vert[color_layer_verts]
                colourList.colours.append(Colour(
                    round(color.x * 255),
                    round(color.y * 255),
                    round(color.z * 255),
                    round(color.w * 255)
                ))
            elif color_layer_loops is not None:
                color = loop[color_layer_loops]
                colourList.colours.append(Colour(
                    round(color.x * 255),
                    round(color.y * 255),
                    round(color.z * 255),
                    round(color.w * 255)
                ))
            else:
                colourList.colours.append(Colour(255,255,255,255))

            oldPrimitiveGroup.numberOfIndices += 1
        
    meshChildren.append(classes.chunks.BoundingBoxChunk.BoundingBoxChunk(low=boundingBoxMin.xzy,high=boundingBoxMax.xzy))
    meshChildren.append(classes.chunks.BoundingSphereChunk.BoundingSphereChunk(center=center.xzy,radius=radius))

    castShadow = 0
    if obj is not None:
        castShadow = int(obj.visible_shadow)

    meshChildren.append(classes.chunks.RenderStatusChunk.RenderStatusChunk(castShadow=castShadow))

    return classes.chunks.MeshChunk.MeshChunk(
        children=meshChildren,
        name=meshName,
        version=0
    )
    