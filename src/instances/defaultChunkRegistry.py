#
# Imports
#

from __future__ import annotations

from classes.chunks.Chunk import Chunk
from classes.chunks.Fence2Chunk import Fence2Chunk
from classes.chunks.FenceChunk import FenceChunk
from classes.chunks.HistoryChunk import HistoryChunk
from classes.chunks.ImageChunk import ImageChunk
from classes.chunks.ImageDataChunk import ImageDataChunk
from classes.chunks.IndexListChunk import IndexListChunk
from classes.chunks.MeshChunk import MeshChunk
from classes.chunks.OldPrimitiveGroupChunk import OldPrimitiveGroupChunk
from classes.chunks.PathChunk import PathChunk
from classes.chunks.PositionListChunk import PositionListChunk
from classes.chunks.ShaderChunk import ShaderChunk
from classes.chunks.ShaderColourParameterChunk import ShaderColourParameterChunk
from classes.chunks.ShaderFloatParameterChunk import ShaderFloatParameterChunk
from classes.chunks.ShaderIntegerParameterChunk import ShaderIntegerParameterChunk
from classes.chunks.ShaderTextureParameterChunk import ShaderTextureParameterChunk
from classes.chunks.StaticEntityChunk import StaticEntityChunk
from classes.chunks.TextureChunk import TextureChunk
from classes.chunks.UVListChunk import UVListChunk
from classes.chunks.StaticPhysChunk import StaticPhysChunk
from classes.chunks.CollisionObjectChunk import CollisionObjectChunk
from classes.chunks.CollisionVolumeChunk import CollisionVolumeChunk
from classes.chunks.CollisionOrientedBoundingBoxChunk import CollisionOrientedBoundingBoxChunk
from classes.chunks.CollisionVectorChunk import CollisionVectorChunk

from classes.ChunkRegistry import ChunkRegistry

import data.chunkIdentifiers as chunkIdentifiers

#
# Default Chunk Registry
#

defaultChunkRegistry = ChunkRegistry()

defaultChunkRegistry.register(chunkIdentifiers.FENCE, FenceChunk)

defaultChunkRegistry.register(chunkIdentifiers.FENCE_2, Fence2Chunk)

defaultChunkRegistry.register(chunkIdentifiers.HISTORY, HistoryChunk)

defaultChunkRegistry.register(chunkIdentifiers.IMAGE, ImageChunk)

defaultChunkRegistry.register(chunkIdentifiers.IMAGE_DATA, ImageDataChunk)

defaultChunkRegistry.register(chunkIdentifiers.INDEX_LIST, IndexListChunk)

defaultChunkRegistry.register(chunkIdentifiers.MESH, MeshChunk)

defaultChunkRegistry.register(chunkIdentifiers.OLD_PRIMITIVE_GROUP, OldPrimitiveGroupChunk)

defaultChunkRegistry.register(chunkIdentifiers.PATH, PathChunk)

defaultChunkRegistry.register(chunkIdentifiers.POSITION_LIST, PositionListChunk)

defaultChunkRegistry.register(chunkIdentifiers.SHADER, ShaderChunk)

defaultChunkRegistry.register(chunkIdentifiers.SHADER_COLOUR_PARAMETER, ShaderColourParameterChunk)

defaultChunkRegistry.register(chunkIdentifiers.SHADER_FLOAT_PARAMETER, ShaderFloatParameterChunk)

defaultChunkRegistry.register(chunkIdentifiers.SHADER_INTEGER_PARAMETER, ShaderIntegerParameterChunk)

defaultChunkRegistry.register(chunkIdentifiers.SHADER_TEXTURE_PARAMETER, ShaderTextureParameterChunk)

defaultChunkRegistry.register(chunkIdentifiers.STATIC_ENTITY, StaticEntityChunk)

defaultChunkRegistry.register(chunkIdentifiers.TEXTURE, TextureChunk)

defaultChunkRegistry.register(chunkIdentifiers.UV_LIST, UVListChunk)

defaultChunkRegistry.register(chunkIdentifiers.STATIC_PHYS, StaticPhysChunk)

defaultChunkRegistry.register(chunkIdentifiers.COLLISION_OBJECT, CollisionObjectChunk)

defaultChunkRegistry.register(chunkIdentifiers.COLLISION_VOLUME, CollisionVolumeChunk)

defaultChunkRegistry.register(chunkIdentifiers.COLLISION_ORIENTED_BOUNDING_BOX, CollisionOrientedBoundingBoxChunk)

defaultChunkRegistry.register(chunkIdentifiers.COLLISION_VECTOR, CollisionVectorChunk)
