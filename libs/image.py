import bpy
import os
import tempfile

from classes.chunks.TextureChunk import TextureChunk
from classes.chunks.ImageChunk import ImageChunk
from classes.chunks.ImageDataChunk import ImageDataChunk

#
# Utility Functions
#

def createImage(chunk: ImageChunk, textureChunk: TextureChunk | None = None):
    for chunkIndex, childChildChunk in enumerate(chunk.children):
        if isinstance(childChildChunk, ImageDataChunk):
            filename = ""
            with tempfile.NamedTemporaryFile(prefix="image",mode="wb+",delete=False) as f:
                f.write(childChildChunk.imageData)
                filename = f.name

            img = bpy.data.images.load(filename)
            img.use_fake_user = True
            img.name = textureChunk.name if textureChunk else chunk.name

            img.pack()

            os.remove(filename)

            return img
