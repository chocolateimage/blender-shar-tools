#
# Imports
#

import bpy
import re

#
# Utility Functions
#

def get_basename(name: str) -> str:
	return re.sub(r"\.\d+$", "", name)

def get_layer_collection_from_collection(collection: bpy.types.Collection, layerCollection: bpy.types.LayerCollection | None = None) -> bpy.types.LayerCollection:
	if layerCollection == None:
		layerCollection = bpy.context.view_layer.layer_collection

	if layerCollection.collection == collection:
		return layerCollection

	for childCollection in layerCollection.children:
		childLayerCollection = get_layer_collection_from_collection(collection, childCollection)
		if childLayerCollection != None:
			return childLayerCollection

	return None
