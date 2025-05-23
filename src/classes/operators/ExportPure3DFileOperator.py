#
# Imports
#

from __future__ import annotations

import os
import tempfile

import bpy
import bpy_extras
import mathutils
import bmesh

import utils

import math

from classes.chunks.FenceChunk import FenceChunk
from classes.chunks.Fence2Chunk import Fence2Chunk
from classes.chunks.ImageChunk import ImageChunk
from classes.chunks.ImageDataChunk import ImageDataChunk
from classes.chunks.TextureChunk import TextureChunk
from classes.chunks.PathChunk import PathChunk
from classes.chunks.ShaderChunk import ShaderChunk
from classes.chunks.ShaderColourParameterChunk import ShaderColourParameterChunk
from classes.chunks.ShaderFloatParameterChunk import ShaderFloatParameterChunk
from classes.chunks.ShaderIntegerParameterChunk import ShaderIntegerParameterChunk
from classes.chunks.ShaderTextureParameterChunk import ShaderTextureParameterChunk
from classes.chunks.StaticEntityChunk import StaticEntityChunk
from classes.chunks.StaticPhysChunk import StaticPhysChunk
from classes.chunks.InstStatEntityChunk import InstStatEntityChunk
from classes.chunks.InstStatPhysChunk import InstStatPhysChunk
from classes.chunks.DynaPhysChunk import DynaPhysChunk
from classes.chunks.InstanceListChunk import InstanceListChunk
from classes.chunks.ScenegraphChunk import ScenegraphChunk
from classes.chunks.OldScenegraphRootChunk import OldScenegraphRootChunk
from classes.chunks.OldScenegraphBranchChunk import OldScenegraphBranchChunk
from classes.chunks.OldScenegraphTransformChunk import OldScenegraphTransformChunk
from classes.chunks.OldScenegraphDrawableChunk import OldScenegraphDrawableChunk
from classes.chunks.OldScenegraphSortOrderChunk import OldScenegraphSortOrderChunk
from classes.chunks.PhysicsObjectChunk import PhysicsObjectChunk
from classes.chunks.GameAttrChunks import GameAttrChunk, GameAttrIntegerParameterChunk

from classes.properties.ShaderProperties import ShaderProperties

from classes.File import File
from classes.Colour import Colour

import libs.mesh as MeshLib
import libs.collision as CollisionLib
import libs.intersect as IntersectLib

#
# Class
#

def collectionItems(self: ExportPure3DFileOperator = None, context: bpy.types.Context = None):
    items = []

    index = 0
    for collection in bpy.data.collections:
        if collection.name.endswith(".p3d"):
            items.append((collection.name,collection.name,"","",index))
            index += 1

    return items

class ExportPure3DFileOperator(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):
    bl_idname = "operators.export_pure3d_file"
    bl_label = "Export Pure3D File."
    bl_description = "Export a Pure3D file from The Simpsons Hit & Run."
    bl_options = {"REGISTER", "UNDO"}

    filename_ext = ".p3d"
    
    collection: bpy.props.EnumProperty(
        name="File Collection",
        description="The collection should contain all things to export and end with \".p3d\"",
        items=collectionItems,
        default=0
        # TODO: Automatically update filename when collection changes
    )
    
    def draw(self, context):
        layout = self.layout

        layout.use_property_decorate = False
        layout.use_property_split = True

        layout.prop(self, "collection")

        if len(collectionItems()) > 0 and os.path.basename(self.filepath) != self.collection:
            layout.label(text="Warning: Filename doesn't match collection name")

    def execute(self, context):
        print("Exporting to " + self.filepath)

        if len(collectionItems()) > 0:
            collection = bpy.data.collections[self.collection]
        else:
            collection = bpy.context.scene.collection
        
        exportedPure3DFile = ExportedPure3DFile(self,self.filepath,collection)

        exportedPure3DFile.export()

        print("Finished exporting")

        return {"FINISHED"}

class RawExportPure3DFileOperator(bpy.types.Operator):
    bl_idname = "operators.raw_export_pure3d_file"
    bl_label = "Export Pure3D File"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH", name="File Path")

    def draw(self, context):
        pass # DO NOT REMOVE else duplicate filepath fields will be shown

    def execute(self, context):
        print("Exporting to " + self.filepath + " from collection " + context.collection.name)
        
        exportedPure3DFile = ExportedPure3DFile(self, self.filepath, context.collection)

        exportedPure3DFile.export()

        print("Finished exporting")

        return {"FINISHED"}

class ExportedPure3DFile():
    def __init__(self, exportPure3DFileOperator: ExportPure3DFileOperator, filePath: str, collection: bpy.types.Collection):
        self.exportPure3DFileOperator = exportPure3DFileOperator

        self.filePath = filePath
        
        self.fileName = os.path.basename(filePath)

        self.collection = collection

        self.textureChunks = []
        self.shaderChunks = []
        self.chunks = []
        
        self.imagesAlreadyExported = []
        self.materialsAlreadyExported = []

        self.intersectFaces = []

    def exportTexture(self, image: bpy.types.Image):
        if image.name in self.imagesAlreadyExported:
            return
        for collection in bpy.data.collections:
            if collection == self.collection:
                continue
            fileCollectionProperties = collection.fileCollectionProperties
            for stickyImage in fileCollectionProperties.sharStickyImages:
                if stickyImage.image.name == image.name:
                    print("Avoiding exporting sticky image " + stickyImage.image.name + " from " + collection.name + " in " + self.collection.name)
                    return
            
        self.imagesAlreadyExported.append(image.name)

        width, height = image.size
        width = pow(2, round(math.log(width, 2)))
        height = pow(2, round(math.log(height, 2)))

        temppath = tempfile.mktemp(prefix="tempbstimage")
        scaledImage = image.copy()
        scaledImage.pixels = image.pixels[:]
        scaledImage.update()
        scaledImage.scale(width, height)
        scaledImage.update()
        scaledImage.save(filepath=temppath)
        bpy.data.images.remove(scaledImage)

        with open(temppath,"rb") as f:
            data = f.read()

        os.remove(temppath)

        self.textureChunks.append(TextureChunk(
            children = [
                ImageChunk(
                    children = [
                        ImageDataChunk(
                            imageData = data
                        )
                    ],
                    name = image.name,
                    version = 14000,
                    width = width,
                    height = height,
                    bitsPerPixel = 8,
                    palettized = 1,
                    hasAlpha = 1,
                    format = ImageChunk.formats["PNG"],
                )
            ],
            version = 14000,
            name = image.name,
            width = width,
            height = height,
            alphaDepth = 8,
            bitsPerPixel = 8,
            textureType = 1,
            usage = 0,
            priority = 0,
            numberOfMipMaps = 1
        ))

    def exportShader(self, mat: bpy.types.Material):
        if mat.name in self.materialsAlreadyExported:
            return
        self.materialsAlreadyExported.append(mat.name)

        shaderProperties: ShaderProperties = mat.shaderProperties

        params = []

        if mat.use_nodes and mat.node_tree is not None and "Principled BSDF" in mat.node_tree.nodes and "Image Texture" in mat.node_tree.nodes and mat.node_tree.nodes["Image Texture"].image is not None:
            imageTexture = mat.node_tree.nodes["Image Texture"]

            self.exportTexture(imageTexture.image)

            params.append(ShaderTextureParameterChunk(parameter="TEX", value=imageTexture.image.name))
        else:
            if shaderProperties.rawTextureName != "":
                params.append(ShaderTextureParameterChunk(parameter="TEX", value=shaderProperties.rawTextureName))

        params.append(ShaderColourParameterChunk(parameter="DIFF", colour=Colour.fromFloatVector(shaderProperties.diffuseColor)))
        params.append(ShaderColourParameterChunk(parameter="SPEC", colour=Colour.fromFloatVector(shaderProperties.specularColor)))
        params.append(ShaderColourParameterChunk(parameter="AMBI", colour=Colour.fromFloatVector(shaderProperties.ambientColor)))
        if mat.use_nodes and mat.node_tree is not None and "Principled BSDF" in mat.node_tree.nodes:
            bsdf = mat.node_tree.nodes["Principled BSDF"]
            params.append(ShaderColourParameterChunk(parameter="EMIS", colour=Colour.fromFloatVector(bsdf.inputs["Emission Color"].default_value)))

        params.append(ShaderIntegerParameterChunk(parameter="2SID", value=shaderProperties.twoSided))
        params.append(ShaderIntegerParameterChunk(parameter="LIT", value=shaderProperties.lighting))
        params.append(ShaderIntegerParameterChunk(parameter="ATST", value=shaderProperties.alphaTest))
        params.append(ShaderIntegerParameterChunk(parameter="BLMD", value=("none","alpha","additive","subtractive").index(shaderProperties.blendMode)))
        params.append(ShaderIntegerParameterChunk(parameter="FIMD", value=("nearestNeighbour","linear","nearestNeighbourMipNN","linearMipNN","linearMipL").index(shaderProperties.filterMode)))
        params.append(ShaderIntegerParameterChunk(parameter="UVMD", value=("tile","clamp").index(shaderProperties.uvMode)))
        params.append(ShaderIntegerParameterChunk(parameter="SHMD", value=("flat","gouraud").index(shaderProperties.shadeMode)))
        params.append(ShaderIntegerParameterChunk(parameter="ACMP", value=("none","always","less","lessEqual","greater","greaterEqual","equal","notEqual").index(shaderProperties.alphaCompare)))
        params.append(ShaderIntegerParameterChunk(parameter="MMIN", value=int(math.log(int(shaderProperties.mipmapMin),2)-3)))
        params.append(ShaderIntegerParameterChunk(parameter="MMAX", value=int(math.log(int(shaderProperties.mipmapMax),2)-3)))

        params.append(ShaderFloatParameterChunk(parameter="SHIN", value=shaderProperties.shininess))
        params.append(ShaderFloatParameterChunk(parameter="ACTH", value=shaderProperties.alphaCompareThreshold))


        # Hardcoded values, probably need to make them dynamic if they actually change
        params.append(ShaderFloatParameterChunk(parameter="CBVV", value=0))
        params.append(ShaderFloatParameterChunk(parameter="MSHP", value=0.5))

        params.append(ShaderIntegerParameterChunk(parameter="CBVA", value=1))
        params.append(ShaderIntegerParameterChunk(parameter="CBVB", value=2))
        params.append(ShaderIntegerParameterChunk(parameter="PLMD", value=0))
        params.append(ShaderIntegerParameterChunk(parameter="CBVM", value=0))
        params.append(ShaderIntegerParameterChunk(parameter="MCBV", value=0))
        params.append(ShaderIntegerParameterChunk(parameter="MMEX", value=0))
    
        params.append(ShaderColourParameterChunk(parameter="CBVC", colour=Colour(255,255,255,255)))

        if shaderProperties.terrainType != "unset":
            self.chunks.append(GameAttrChunk(
                name = mat.name,
                children = [
                    GameAttrIntegerParameterChunk(
                        parameter="TerrainType",
                        value=int(shaderProperties.terrainType)
                    )
                ]
            ))

        self.shaderChunks.append(ShaderChunk(
            children = params,
            name = mat.name,
            version = 0,
            pddiShaderName = shaderProperties.pddiShader,
            hasTranslucency = mat.blend_method == "HASHED",
        ))
    
    def addAsInterset(self, mesh: bpy.types.Mesh):
        if "track" not in mesh.name and "polySurfaceShape" not in mesh.name:
            return
        if len(mesh.materials) == 0:
            return
        shaderProperties: ShaderProperties = mesh.materials[0].shaderProperties
        if shaderProperties.terrainType == "unset":
            return
        bm = bmesh.new()
        bm.from_mesh(mesh)

        bmesh.ops.triangulate(bm, faces=bm.faces[:])

        bm.verts.ensure_lookup_table()
        bm.edges.ensure_lookup_table()
        bm.faces.ensure_lookup_table()

        for face in bm.faces:
            positions = []
            for i in [0,2,1]:
                loop = face.loops[i]
                positions.append(loop.vert.co.xzy)
            self.intersectFaces.append(IntersectLib.Face(positions,int(shaderProperties.terrainType)))

    def export(self):
        fileCollectionProperties = self.collection.fileCollectionProperties
        for stickyImage in fileCollectionProperties.sharStickyImages:
            self.exportTexture(stickyImage.image)

        for childCollection in self.collection.children:
            collectionBasename = utils.get_basename(childCollection.name)
    
            if collectionBasename == "Fences":
                for fence in childCollection.all_objects:
                    if not fence.isFence:
                        continue

                    fenceCurve: bpy.types.Curve = fence.data

                    fenceCurveSpline = fenceCurve.splines[0]

                    start = fenceCurveSpline.points[0].co.xzy
                    end = fenceCurveSpline.points[1].co.xzy

                    calculatedNormal = (end - start).cross(mathutils.Vector((0, 1, 0))).normalized()

                    calculatedNormal.y = 0

                    if fence.fenceProperties.isFlipped:
                        calculatedNormal = -calculatedNormal

                    self.chunks.append(FenceChunk(children=[
                        Fence2Chunk(
                            start=start,
                            end=end,
                            normal=calculatedNormal
                        )
                    ]))
            elif collectionBasename == "Paths":
                for path in childCollection.all_objects:
                    if not path.isPath:
                        continue

                    pathCurve = path.data
                    pathCurveSpline = pathCurve.splines[0]

                    points = []

                    for point in pathCurveSpline.points:
                        points.append(point.co.xzy)
                    
                    self.chunks.append(PathChunk(
                        points = points
                    ))
            elif collectionBasename == "Static Entities":
                for obj in childCollection.objects:
                    mesh = obj.data
                    hasAlpha = 0
                    for mat in mesh.materials:
                        self.exportShader(mat)
                        shaderProperties: ShaderProperties = mat.shaderProperties
                        if shaderProperties.blendMode == "alpha" or shaderProperties.alphaTest:
                            hasAlpha = 1

                    chunk = MeshLib.meshToChunk(mesh, obj)
                    self.addAsInterset(mesh)
                    self.chunks.append(StaticEntityChunk(
                        version = 0,
                        hasAlpha = hasAlpha,
                        name = obj.name,
                        children = [
                            chunk
                        ]
                    ))
            elif collectionBasename == "Collisions":
                collisionGroups = {}
                for obj in childCollection.all_objects:
                    baseName = utils.get_basename(obj.name)
                    if baseName not in collisionGroups:
                        collisionGroups[baseName] = []
                    collisionGroups[baseName].append(obj)
                
                for groupName, group in collisionGroups.items():
                    collisionChildren = CollisionLib.collisionsToChunks(groupName, group)
                    self.chunks.append(
                        StaticPhysChunk(
                            name = groupName,
                            children = collisionChildren
                        )
                    )
            elif collectionBasename == "Instanced":
                for instancedCollection in childCollection.children:
                    alreadyExportedMeshes = {}
                    children = []
                    has_collisions = False
                    has_physics = False

                    for obj in instancedCollection.objects:
                        mesh = obj.data
                        meshName = utils.get_basename(mesh.name)
                        if meshName in alreadyExportedMeshes:
                            alreadyExportedMeshes[meshName].append(obj)
                            continue
                        alreadyExportedMeshes[meshName] = [obj]

                        for mat in mesh.materials:
                            self.exportShader(mat)

                        meshChunk = MeshLib.meshToChunk(mesh,obj)
                        children.append(meshChunk)
                    

                    for instancedCollectionChild in instancedCollection.children:
                        instancedCollectionChildBasename = utils.get_basename(instancedCollectionChild.name)
                        if instancedCollectionChildBasename == "Collisions":
                            collisionGroups = {}
                            for obj in instancedCollectionChild.objects:
                                baseName = utils.get_basename(obj.name)
                                if baseName not in collisionGroups:
                                    collisionGroups[baseName] = []
                                collisionGroups[baseName].append(obj)
                            
                            for groupName, group in collisionGroups.items():
                                childrenToAdd = CollisionLib.collisionsToChunks(groupName, group)
                                children.extend(childrenToAdd)
                                has_collisions = True
                                for c in childrenToAdd:
                                    if isinstance(c, PhysicsObjectChunk):
                                        has_physics = True
                                

                    instanceList = InstanceListChunk()
                    instanceList.name = utils.get_basename(instancedCollection.name)
                    for meshName in alreadyExportedMeshes:
                        scenegraph = ScenegraphChunk(name=meshName)
                        root = OldScenegraphRootChunk()
                        rootBranch = OldScenegraphBranchChunk()
                        rootBranch.name = "root"
                        rootTransform = OldScenegraphTransformChunk()
                        rootTransform.name = meshName
                        for obj in alreadyExportedMeshes[meshName]:
                            obj: bpy.types.Object
                            transform = OldScenegraphTransformChunk()
                            transform.name = obj.name
                            location, rotation, scale = obj.matrix_world.decompose()
                            location = location.xzy
                            rotation_euler: mathutils.Euler = rotation.to_euler()
                            rotation_euler = mathutils.Euler((-rotation_euler.x,-rotation_euler.z,-rotation_euler.y),"ZXY")
                            rotation = rotation_euler.to_quaternion()
                            transform.matrix = mathutils.Matrix.LocRotScale(location, rotation, scale).transposed()

                            drawable = OldScenegraphDrawableChunk()
                            drawable.name = meshName
                            drawable.drawableName = meshName
                            drawable.isTranslucent = 0

                            sortOrder = OldScenegraphSortOrderChunk(sortOrder=0.5)
                            drawable.children.append(sortOrder)

                            transform.children.append(drawable)

                            rootTransform.children.append(transform)

                        rootBranch.children.append(rootTransform)
                        root.children.append(rootBranch)
                        scenegraph.children.append(root)
                        instanceList.children.append(scenegraph)
                    
                    children.append(instanceList)

                    chunkType = InstStatEntityChunk
                    if has_collisions:
                        chunkType = InstStatPhysChunk
                        if has_physics:
                            chunkType = DynaPhysChunk

                    self.chunks.append(
                        chunkType(
                            children=children,
                            name=instancedCollection.name,
                            version=0,
                            hasAlpha=0
                        )
                    )



        chunks = []
        chunks.extend(self.textureChunks)
        chunks.extend(self.shaderChunks)
        chunks.extend(self.chunks)
        chunks.extend(IntersectLib.convertToChunks(self.intersectFaces))
        b = File.toBytes(chunks) # don't do it directly in the with context to not make a file when an error occurs
        with open(self.filePath,"wb+") as f:
            f.write(b)
    
def menu_item(self, context):
    self.layout.operator(ExportPure3DFileOperator.bl_idname, text = "Pure3D File (.p3d)")

def register():
    bpy.utils.register_class(ExportPure3DFileOperator)
    bpy.utils.register_class(RawExportPure3DFileOperator)
    
    bpy.types.TOPBAR_MT_file_export.append(menu_item)

def unregister():
    bpy.utils.unregister_class(ExportPure3DFileOperator)
    bpy.utils.unregister_class(RawExportPure3DFileOperator)

    bpy.types.TOPBAR_MT_file_export.remove(menu_item)
