#
# Imports
#

import bpy

import classes.chunks.Chunk
import classes.chunks.IndexListChunk
import classes.chunks.MeshChunk
import classes.chunks.OldPrimitiveGroupChunk
import classes.chunks.PositionListChunk
import classes.chunks.UVListChunk

#
# Utility Functions
#

def createMesh(chunk: classes.chunks.MeshChunk.MeshChunk) -> bpy.types.Mesh:
	mesh = bpy.data.meshes.new(chunk.name + "Mesh")

	total_positions = []
	total_indices = []
	total_uvs = []

	indexoffset = 0
	separators = [0]
	for childChunkIndex, childChunk in enumerate(chunk.children):

		if isinstance(childChunk, classes.chunks.OldPrimitiveGroupChunk.OldPrimitiveGroupChunk):
			if childChunk.shaderName in bpy.data.materials:
				mesh.materials.append(bpy.data.materials[childChunk.shaderName])

			for childChildChunkIndex, childChildChunk in enumerate(childChunk.children):
				
				if isinstance(childChildChunk,classes.chunks.PositionListChunk.PositionListChunk):
					for position in childChildChunk.positions:
						total_positions.append((position.x,position.z,position.y))
				
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

		indexoffset += len(total_positions)
		separators.append(len(total_indices))

	mesh.from_pydata(total_positions,[],total_indices)
	mesh.update()
	
	uvLayer = mesh.uv_layers.new()

	for i,poly in enumerate(mesh.polygons):
		for k,j in enumerate(separators):
			if i >= j:
				poly.material_index = k
				continue
		for loop_index in poly.loop_indices:
			loop = mesh.loops[loop_index]
			vertex_index = loop.vertex_index
			if vertex_index < len(total_uvs):
				uv = total_uvs[vertex_index]
				uvLayer.data[loop_index].uv = uv
			else:
				print(mesh.name)
	
	
	mesh.update()

	return mesh