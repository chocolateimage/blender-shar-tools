import bpy
import re
import textwrap

#
# Utility Functions
#

def get_basename(name: str) -> str:
    return re.sub(r"\.\d+$", "", name)

def get_layer_collection_from_collection(collection: bpy.types.Collection, layerCollection: bpy.types.LayerCollection | None = None) -> bpy.types.LayerCollection:
    if layerCollection is None:
        layerCollection = bpy.context.view_layer.layer_collection

    if layerCollection.collection == collection:
        return layerCollection

    for childCollection in layerCollection.children:
        childLayerCollection = get_layer_collection_from_collection(collection, childCollection)
        if childLayerCollection is not None:
            return childLayerCollection

    return None

def layout_wrapped_label(layout: bpy.types.UILayout, context: bpy.types.Context, text: str):
    width = context.region.width

    line_length = int(width / 7)

    lines = textwrap.wrap(text, width=line_length)

    if len(lines) == 0:
        return

    col = layout.column()
    col.scale_y = 0.7

    for i in lines:
        col.label(text=i)

def get_blender_version():
    """Gets the Blender release version as a high number to be able to be used in if checks

    Returns:
        int: Major * 10000 + Minor * 100 + Micro * 1
    """

    return bpy.app.version[0] * 10000 + bpy.app.version[1] * 100 + bpy.app.version[2]
