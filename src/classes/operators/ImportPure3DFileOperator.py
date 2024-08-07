#
# Imports
#

from __future__ import annotations

import os

import bpy
import bpy_extras

from classes.chunks.Chunk import Chunk
from classes.chunks.FenceChunk import FenceChunk
from classes.chunks.Fence2Chunk import Fence2Chunk
from classes.chunks.HistoryChunk import HistoryChunk
from classes.chunks.ImageChunk import ImageChunk
from classes.chunks.TextureChunk import TextureChunk
from classes.chunks.MeshChunk import MeshChunk
from classes.chunks.PathChunk import PathChunk
from classes.chunks.ShaderChunk import ShaderChunk
from classes.chunks.ShaderColourParameterChunk import ShaderColourParameterChunk
from classes.chunks.ShaderFloatParameterChunk import ShaderFloatParameterChunk
from classes.chunks.ShaderIntegerParameterChunk import ShaderIntegerParameterChunk
from classes.chunks.ShaderTextureParameterChunk import ShaderTextureParameterChunk
from classes.chunks.StaticEntityChunk import StaticEntityChunk
from classes.chunks.StaticPhysChunk import StaticPhysChunk
from classes.chunks.CollisionObjectChunk import CollisionObjectChunk
from classes.chunks.InstStatEntityChunk import InstStatEntityChunk
from classes.chunks.InstStatPhysChunk import InstStatPhysChunk
from classes.chunks.DynaPhysChunk import DynaPhysChunk
from classes.chunks.InstanceListChunk import InstanceListChunk
from classes.chunks.ScenegraphChunk import ScenegraphChunk
from classes.chunks.OldScenegraphBranchChunk import OldScenegraphBranchChunk
from classes.chunks.OldScenegraphDrawableChunk import OldScenegraphDrawableChunk
from classes.chunks.OldScenegraphRootChunk import OldScenegraphRootChunk
from classes.chunks.OldScenegraphSortOrderChunk import OldScenegraphSortOrderChunk
from classes.chunks.OldScenegraphTransformChunk import OldScenegraphTransformChunk

from classes.File import File

import libs.fence as FenceLib
import libs.image as ImageLib
import libs.mesh as MeshLib
import libs.message as MessageLib
import libs.path as PathLib
import libs.collision as CollisionLib

import mathutils
import math

import utils

#
# Class
#

class ImportPure3DFileOperator(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):
	bl_idname = "operators.import_pure3d_file"
	bl_label = "Import Pure3D File(s)..."
	bl_description = "Import Pure3D File(s) from The Simpsons Hit & Run."
	bl_options = {"REGISTER", "UNDO"}

	filename_ext = ".p3d"

	directory: bpy.props.StringProperty(subtype = "DIR_PATH", options = {"HIDDEN"})
	filter_glob: bpy.props.StringProperty(default = "*.p3d", options = {"HIDDEN"}, maxlen = 255)
	files: bpy.props.CollectionProperty(type = bpy.types.OperatorFileListElement, options = {"HIDDEN", "SKIP_SAVE"})

	option_import_textures: bpy.props.BoolProperty(name = "Import Textures", description = "Import Texture chunks from the Pure3D File(s)", default = True)
	option_import_shaders: bpy.props.BoolProperty(name = "Import Shaders", description = "Import Shader chunks from the Pure3D File(s)", default = True)
	option_import_fences: bpy.props.BoolProperty(name = "Import Fences", description = "Import Fence chunks from the Pure3D File(s)", default = True)
	option_import_paths: bpy.props.BoolProperty(name = "Import Paths", description = "Import Path chunks from the Pure3D File(s)", default = True)
	option_import_static_entities: bpy.props.BoolProperty(name = "Import Static Entities", description = "Import StaticEntity chunks from the Pure3D File(s)", default = True)
	option_import_collisions: bpy.props.BoolProperty(name = "Import Collisions", description = "Import StaticPhys chunks from the Pure3D File(s)", default = True)

	def draw(self, context):
		self.layout.prop(self, "option_import_textures")

		self.layout.prop(self, "option_import_shaders")

		self.layout.prop(self, "option_import_fences")

		self.layout.prop(self, "option_import_paths")

		self.layout.prop(self, "option_import_static_entities")

		self.layout.prop(self, "option_import_collisions")

	def execute(self, context):
		print(self.files)

		importedPure3DFiles : list[ImportedPure3DFile] = []

		for file in self.files:
			filePath = os.path.join(self.directory, file.name)

			importedPure3DFile = self.importPure3DFile(filePath)

			importedPure3DFiles.append(importedPure3DFile)

		self.showMessage(importedPure3DFiles)

		return {"FINISHED"}

	def importPure3DFile(self, filePath) -> ImportedPure3DFile:
		#
		# Read Pure3D File
		#

		with open(filePath, "rb") as file:
			fileContents = file.read()

		rootChunk = File.fromBytes(fileContents)

		#
		# Import Pure3D File
		#

		importedPure3DFile = ImportedPure3DFile(self, filePath, rootChunk.children)

		importedPure3DFile.importChunks()

		#
		# Return
		#

		return importedPure3DFile

	def showMessage(self, importedPure3DFiles : list[ImportedPure3DFile]):
		messageLines : list[str] = []

		messageLines.append(f"Imported { len(importedPure3DFiles) } Pure3D File(s):")

		for importedPure3DFile in importedPure3DFiles:
			messageLines.append(f"- { importedPure3DFile.fileName }:")
	
			if importedPure3DFile.numberOfTextureChunksImported > 0:
				messageLines.append(f"\t- Number of Textures: { importedPure3DFile.numberOfTextureChunksImported }")

			if importedPure3DFile.numberOfShaderChunksImported > 0:
				messageLines.append(f"\t- Number of Shaders: { importedPure3DFile.numberOfShaderChunksImported }")

			if importedPure3DFile.numberOfFenceChunksImported > 0:
				messageLines.append(f"\t- Number of Fences: { importedPure3DFile.numberOfFenceChunksImported }")

			if importedPure3DFile.numberOfPathChunksImported > 0:
				messageLines.append(f"\t- Number of Paths: { importedPure3DFile.numberOfPathChunksImported }")

			if importedPure3DFile.numberOfStaticEntityChunksImported > 0:
				messageLines.append(f"\t- Number of Static Entities: { importedPure3DFile.numberOfStaticEntityChunksImported }")

			if importedPure3DFile.numberOfCollisionsImported > 0:
				messageLines.append(f"\t- Number of Collisions: { importedPure3DFile.numberOfCollisionsImported }")

			if importedPure3DFile.numberOfInstancedImported > 0:
				messageLines.append(f"\t- Number of Instanced Chunks: { importedPure3DFile.numberOfInstancedImported }")

			if importedPure3DFile.numberOfUnsupportedChunksSkipped > 0:
				messageLines.append(f"\t- Number of Unsupported Chunks: { importedPure3DFile.numberOfUnsupportedChunksSkipped }")

		MessageLib.alert("\n".join(messageLines))

		print("\n".join(messageLines))

class ImportedPure3DFile():
	def __init__(self, importPure3DFileOperator : ImportPure3DFileOperator, filePath : str, chunks : list[Chunk]):
		self.importPure3DFileOperator = importPure3DFileOperator

		self.chunks = chunks

		self.filePath = filePath
		
		self.fileName = os.path.basename(filePath)
	
		self.fenceCollection : bpy.types.Collection = bpy.data.collections.new("Fences")

		self.pathCollection : bpy.types.Collection = bpy.data.collections.new("Paths")

		self.staticEntityCollection : bpy.types.Collection = bpy.data.collections.new("Static Entities")
	
		self.collisionCollection : bpy.types.Collection = bpy.data.collections.new("Collisions")

		self.instancedCollection : bpy.types.Collection = bpy.data.collections.new("Instanced")

		self.numberOfTextureChunksImported : int = 0

		self.numberOfShaderChunksImported : int = 0

		self.numberOfFenceChunksImported : int = 0

		self.numberOfPathChunksImported : int = 0

		self.numberOfStaticEntityChunksImported : int = 0

		self.numberOfCollisionsImported : int = 0

		self.numberOfInstancedImported : int = 0

		self.numberOfUnsupportedChunksSkipped : int = 0

		self.collectionsToHide = []

	def importChunks(self) -> None:
		#
		# Print
		#

		print(f"Importing chunks from Pure3D File: { self.filePath }")

		#
		# Iterate Chunks
		#

		for chunkIndex, chunk in enumerate(self.chunks):
			if isinstance(chunk, FenceChunk):
				if self.importPure3DFileOperator.option_import_fences:
					self.importFenceChunk(chunkIndex, chunk)

			elif isinstance(chunk, PathChunk):
				if self.importPure3DFileOperator.option_import_paths:
					self.importPathChunk(chunkIndex, chunk)

			elif isinstance(chunk, ShaderChunk):
				if self.importPure3DFileOperator.option_import_shaders:
					self.importShaderChunk(chunk)

			elif isinstance(chunk, StaticEntityChunk):
				if self.importPure3DFileOperator.option_import_static_entities:
					self.importStaticEntityChunk(chunk)

			elif isinstance(chunk, TextureChunk):
				if self.importPure3DFileOperator.option_import_textures:
					self.importTextureChunk(chunk)
			
			elif isinstance(chunk, StaticPhysChunk):
				if self.importPure3DFileOperator.option_import_collisions:
					self.importStaticPhysChunk(chunk)

			elif isinstance(chunk, InstStatEntityChunk):
				self.importInstancedChunk(chunk)

			elif isinstance(chunk, InstStatPhysChunk):
				self.importInstancedChunk(chunk)

			elif isinstance(chunk, DynaPhysChunk):
				self.importInstancedChunk(chunk)

			else:
				print(f"Unsupported chunk type: { hex(chunk.identifier) }")

				self.numberOfUnsupportedChunksSkipped += 1

		#
		# Create File Collection
		#

		if self.numberOfFenceChunksImported == 0 and self.numberOfPathChunksImported == 0 and self.numberOfStaticEntityChunksImported == 0 and self.numberOfCollisionsImported == 0 and self.numberOfInstancedImported == 0:
			return

		fileCollection = bpy.data.collections.new(self.fileName)

		bpy.context.scene.collection.children.link(fileCollection)
		
		if self.numberOfFenceChunksImported > 0:
			fileCollection.children.link(self.fenceCollection)
		else:
			bpy.data.collections.remove(self.fenceCollection)

		if self.numberOfPathChunksImported > 0:
			fileCollection.children.link(self.pathCollection)
		else:
			bpy.data.collections.remove(self.pathCollection)

		if self.numberOfStaticEntityChunksImported > 0:
			fileCollection.children.link(self.staticEntityCollection)
		else:
			bpy.data.collections.remove(self.staticEntityCollection)

		if self.numberOfCollisionsImported > 0:
			fileCollection.children.link(self.collisionCollection)
		else:
			bpy.data.collections.remove(self.collisionCollection)

		if self.numberOfInstancedImported > 0:
			fileCollection.children.link(self.instancedCollection)
		else:
			bpy.data.collections.remove(self.instancedCollection)
		
		for collection in self.collectionsToHide:
			utils.get_layer_collection_from_collection(collection).hide_viewport = True

	def importInstancedChunk(self, chunk: Chunk):
		
		instancedCollection = bpy.data.collections.new(chunk.name) # Not to be confused with "Instance Collection" or self.instancedCollection
		self.instancedCollection.children.link(instancedCollection)

		instanceList: InstanceListChunk = chunk.getFirstChildOfType(InstanceListChunk)

		meshes = {}
		collisions = {}

		for meshChunk in chunk.getChildrenOfType(MeshChunk):
			meshes[meshChunk.name] = MeshLib.createMesh(meshChunk)

		for collisionObjectChunk in chunk.getChildrenOfType(CollisionObjectChunk):
			collisionCollection = bpy.data.collections.new("Collisions")
			self.collectionsToHide.append(collisionCollection)
			instancedCollection.children.link(collisionCollection)

			collisions[collisionObjectChunk.name] = CollisionLib.createCollision(collisionObjectChunk)
			for collisionObject in collisions[collisionObjectChunk.name]:
				collisionObject: bpy.types.Object
				collisionCollection.objects.link(collisionObject)

		scenegraph = instanceList.getFirstChildOfType(ScenegraphChunk)
		root = scenegraph.getFirstChildOfType(OldScenegraphRootChunk)
		rootBranch = root.getFirstChildOfType(OldScenegraphBranchChunk)
		rootTransform = rootBranch.getFirstChildOfType(OldScenegraphTransformChunk)

		for transform in rootTransform.getChildrenOfType(OldScenegraphTransformChunk):
			transform: OldScenegraphTransformChunk
			drawable: OldScenegraphDrawableChunk = transform.getFirstChildOfType(OldScenegraphDrawableChunk)

			mesh = meshes[drawable.drawableName]

			obj = bpy.data.objects.new(transform.name, mesh)

			obj.matrix_world = transform.matrix.transposed()
			obj.location = obj.location.xzy
			obj.rotation_euler = mathutils.Euler((obj.rotation_euler.x,obj.rotation_euler.z,-obj.rotation_euler.y))
			obj.scale = obj.scale.xzy

			instancedCollection.objects.link(obj)
		
		self.numberOfInstancedImported += 1

	def importFenceChunk(self, chunkIndex : int, chunk : FenceChunk) -> None:
		for childChunkIndex, childChunk in enumerate(chunk.children):
			if isinstance(childChunk, Fence2Chunk):
				fenceChunkObject = FenceLib.createFence(childChunk.start, childChunk.end, childChunk.normal, f"Fence { chunkIndex }")

				self.fenceCollection.objects.link(fenceChunkObject)

				self.numberOfFenceChunksImported += 1

	def importPathChunk(self, chunkIndex : int, chunk : PathChunk) -> None:
		pathChunkObject = PathLib.createPath(chunk.points, f"Path { chunkIndex }")

		self.pathCollection.objects.link(pathChunkObject)

		self.numberOfPathChunksImported += 1

	def importShaderChunk(self, chunk : ShaderChunk) -> None:
		if chunk.name in bpy.data.materials:
			# TODO: Consider keeping track of this and informing the user
			# 	Maybe only if the shader is meaningfully different?
			# 	Regions all have their own shaders so this would be a lot of spam otherwise
			return

		material = bpy.data.materials.new(chunk.name)

		material.use_fake_user = True # Save material even when it's not used

		material.use_nodes = True

		material.shaderProperties.pddiShader = chunk.pddiShaderName
		
		bsdf = material.node_tree.nodes["Principled BSDF"]

		if chunk.hasTranslucency:
			material.blend_method = "HASHED"

			material.shadow_method = "HASHED"

		for childChunkIndex, childChunk in enumerate(chunk.children):
			if isinstance(childChunk, ShaderTextureParameterChunk):
				if childChunk.parameter == "TEX":
					if childChunk.value not in bpy.data.images:
						print("Image",childChunk.value,"not found to apply on a material")
						continue

					image = bpy.data.images[childChunk.value]

					texture_image = material.node_tree.nodes.new("ShaderNodeTexImage")
					texture_image.image = image
					
					material.node_tree.links.new(bsdf.inputs["Base Color"],texture_image.outputs["Color"])
					material.node_tree.links.new(bsdf.inputs["Alpha"],texture_image.outputs["Alpha"]) # Always connect alpha nodes, transparency only visible when blend method is set to "Alpha Hashed"
			
			elif isinstance(childChunk, ShaderColourParameterChunk):
				# hacky way to do it
				color_argb = (childChunk.colour.red / 255,childChunk.colour.green / 255,childChunk.colour.blue / 255,childChunk.colour.alpha / 255)
				color_rgb = (childChunk.colour.red / 255,childChunk.colour.green / 255,childChunk.colour.blue / 255)
				if childChunk.parameter == "DIFF":
					bsdf.inputs[0].default_value = color_argb # Diffusive Color
					material.shaderProperties.diffuseColor = color_rgb # Specular
				elif childChunk.parameter == "SPEC":
					material.shaderProperties.specularColor = color_rgb # Specular
				elif childChunk.parameter == "AMBI":
					material.shaderProperties.ambientColor = color_rgb # Ambient
				elif childChunk.parameter == "EMIS":
					bsdf.inputs[26].default_value = color_argb # Emission Color
					bsdf.inputs[27].default_value = 1 # Emission Strength
				else:
					pass
			
			elif isinstance(childChunk, ShaderIntegerParameterChunk):
				if childChunk.parameter == "2SID":
					material.shaderProperties.twoSided = childChunk.value
					material.use_backface_culling = not childChunk.value
				elif childChunk.parameter == "LIT":
					material.shaderProperties.lighting = childChunk.value == 1
				elif childChunk.parameter == "ATST":
					material.shaderProperties.alphaTest = childChunk.value == 1
				elif childChunk.parameter == "BLMD":
					material.shaderProperties.blendMode = ("none","alpha","additive","subtractive")[childChunk.value]
				elif childChunk.parameter == "FIMD":
					material.shaderProperties.filterMode = ("nearestNeighbour","linear","nearestNeighbourMipNN","linearMipNN","linearMipL")[childChunk.value]
				elif childChunk.parameter == "UVMD":
					material.shaderProperties.uvMode = ("tile","clamp")[childChunk.value]
				elif childChunk.parameter == "SHMD":
					material.shaderProperties.shadeMode = ("flat","gouraud")[childChunk.value]
				elif childChunk.parameter == "ACMP":
					material.shaderProperties.alphaCompare = ("none","always","less","lessEqual","greater","greaterEqual","equal","notEqual")[childChunk.value]
				elif childChunk.parameter == "MMIN":
					material.shaderProperties.mipmapMin = str(pow(2,3+childChunk.value))
				elif childChunk.parameter == "MMAX":
					material.shaderProperties.mipmapMax = str(pow(2,3+childChunk.value))
				else:
					pass
			
			elif isinstance(childChunk, ShaderFloatParameterChunk):
				if childChunk.parameter == "SHIN":
					material.shaderProperties.shininess = childChunk.value
				elif childChunk.parameter == "ACTH":
					material.shaderProperties.alphaCompareThreshold = childChunk.value
				else:
					pass
	
		self.numberOfShaderChunksImported += 1

	def importStaticEntityChunk(self, chunk : StaticEntityChunk) -> None:
		# TODO: I am pretty sure static entities are only allowed to contain one mesh
		#	So this code should make that assumption, I think, and maybe error otherwise (< 1 or > 1)
		for childChunk in chunk.children:
			if isinstance(childChunk, MeshChunk):
				mesh = MeshLib.createMesh(childChunk)

				meshObject = bpy.data.objects.new(chunk.name, mesh)

				self.staticEntityCollection.objects.link(meshObject)

				self.numberOfStaticEntityChunksImported += 1

	def importTextureChunk(self, chunk : TextureChunk) -> None:
		for i in bpy.data.images:
			if i.name == chunk.name:
				return

		# TODO: Pretty sure this is currently fucked if the P3D has mipmaps for whatever reason
		for childChunk in chunk.children:
			if isinstance(childChunk, ImageChunk):
				ImageLib.createImage(childChunk, chunk)

		self.numberOfTextureChunksImported += 1
	
	def importStaticPhysChunk(self, chunk: StaticPhysChunk):
		for childChunk in chunk.children:
			if isinstance(childChunk,CollisionObjectChunk):
				objects = CollisionLib.createCollision(childChunk)
				for i in objects:
					self.collisionCollection.objects.link(i)
					self.numberOfCollisionsImported += 1

def menu_item(self, context):
	self.layout.operator(ImportPure3DFileOperator.bl_idname, text = "Pure3D File (.p3d)")

def register():
	bpy.utils.register_class(ImportPure3DFileOperator)
	
	bpy.types.TOPBAR_MT_file_import.append(menu_item)

def unregister():
	bpy.utils.unregister_class(ImportPure3DFileOperator)

	bpy.types.TOPBAR_MT_file_import.remove(menu_item)
