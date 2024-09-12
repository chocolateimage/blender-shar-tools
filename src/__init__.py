#
# Blender Add-on Metadata
#

bl_info = {
    "name": "The Simpsons Hit & Run Tools",
    "description": "A collection of tools to help mod The Simpsons Hit & Run.",
    "author": "Donut Team",
    "version": (1, 0, 0),
    "blender": (4, 1, 1),
    "location": "TODO",
    "doc_url": "https://donutteam.com", # TODO: Actual documentation URL
    "tracker_url": "https://github.com/donutteam/blender-shar-tools/issues",
    "category": "Import-Export",
}

#
# Add Add-on Directory to Path
#

import os
import sys

sys.path.append(os.path.dirname(__file__))

#
# Imports
#

import bpy

import classes.operators.AddCollisionOperator
import classes.operators.ImportPure3DFileOperator
import classes.operators.ExportPure3DFileOperator

import classes.Pure3DFileHandler

import classes.properties.FenceProperties
import classes.properties.ShaderProperties
import classes.properties.PathProperties
import classes.properties.CollisionProperties
import classes.properties.FileCollectionProperties

#
# Initialisation
#

def register():
    print("Registered The Simpsons Hit & Run Tools.")

    classes.operators.ImportPure3DFileOperator.register()
    classes.operators.ExportPure3DFileOperator.register()
    classes.Pure3DFileHandler.register()

    classes.operators.AddCollisionOperator.register()

    classes.properties.FenceProperties.register()
    classes.properties.PathProperties.register()
    classes.properties.ShaderProperties.register()
    classes.properties.CollisionProperties.register()
    classes.properties.FileCollectionProperties.register()

def unregister():
    print("Unregistered The Simpsons Hit & Run Tools.")

    classes.operators.ImportPure3DFileOperator.unregister()
    classes.operators.ExportPure3DFileOperator.unregister()
    classes.Pure3DFileHandler.unregister()

    classes.operators.AddCollisionOperator.unregister()

    classes.properties.FenceProperties.unregister()
    classes.properties.PathProperties.unregister()
    classes.properties.ShaderProperties.unregister()
    classes.properties.CollisionProperties.unregister()
    classes.properties.FileCollectionProperties.unregister()
