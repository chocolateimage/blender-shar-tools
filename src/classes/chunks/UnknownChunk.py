#
# Imports
#

from __future__ import annotations

import typing

import classes.chunks.Chunk

import classes.Pure3DBinaryReader
import classes.Pure3DBinaryWriter

#
# Class
#

class UnknownChunkOptions(typing.TypedDict):
	identifier : int

	children : list[Chunk]

	data : bytes | None

class UnknownChunk(classes.chunks.Chunk.Chunk):
	@staticmethod
	def parseData(options : classes.chunks.Chunk.ChunkParseDataOptions) -> dict:	
		return {
			"data": options["data"],
		}

	def __init__(self, options : UnknownChunkOptions) -> None:
		super().__init__(options)

		print("UnknownChunk", "identifier", options["identifier"], "len(data)", len(options["data"]))

		self.data : bytes = options["data"]

	def writeData(self, binaryWriter : classes.Pure3DBinaryWriter.Pure3DBinaryWriter) -> None:
		if self.data is not None:
			binaryWriter.writeBytes(self.data)