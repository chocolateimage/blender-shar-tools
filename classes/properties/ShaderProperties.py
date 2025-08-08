#
# Imports
#

import bpy

#
# Class
#


def update_shader_properties(self, context: bpy.types.Context):
    mat = getattr(self,"id_data",None) # for some weird reason the material is in "id_data" but not in context when updated from a script
    if mat is None:
        return

    if mat.shaderProperties.blendMode == "alpha" or mat.shaderProperties.alphaTest:
        mat.blend_method = "HASHED"
        if hasattr(mat, "shadow_method"):
            mat.shadow_method = "HASHED"
        try:
            bsdf = mat.node_tree.nodes["Principled BSDF"]
            texture_image = mat.node_tree.nodes["Image Texture"]
            mat.node_tree.links.new(bsdf.inputs["Alpha"],texture_image.outputs["Alpha"])
        except Exception as e:
            print(e)
    else:
        mat.blend_method = "OPAQUE"
        if hasattr(mat, "shadow_method"):
            mat.shadow_method = "OPAQUE"
    
    mat.use_backface_culling = not mat.shaderProperties.twoSided


class ShaderProperties(bpy.types.PropertyGroup):
    pddiShader: bpy.props.EnumProperty(
        name="PDDI Shader",
        items=[
            (v,v,"","",i) for i,v in enumerate(["error","simple", "lightweight", "lightmap", "environment", "spheremap", "projtex", "pointsprite", "layered", "layeredlmap", "toon", "hctune"])
        ],
        default=1
    )
    diffuseColor: bpy.props.FloatVectorProperty(
        name="Diffuse",
        min=0,
        max=1,
        subtype="COLOR",
        default=(1,1,1)
    )
    specularColor: bpy.props.FloatVectorProperty(
        name="Specular",
        min=0,
        max=1,
        subtype="COLOR",
    )
    ambientColor: bpy.props.FloatVectorProperty(
        name="Ambient",
        min=0,
        max=1,
        subtype="COLOR",
    )
    blendMode: bpy.props.EnumProperty(
        name="Blend Mode",
        items=[
            ("none","None","","",0),
            ("alpha","Alpha","","",1),
            ("additive","Additive","","",2),
            ("subtractive","Subtractive","","",3),
        ],
        update=update_shader_properties
    )
    filterMode: bpy.props.EnumProperty(
        name="Filter Mode",
        items=[
            ("nearestNeighbour","Nearest Neighbour","None","",0),
            ("linear","Linear","Bilinear","",1),
            ("nearestNeighbourMipNN","Nearest Neighbour, Mip Nearest Neighbour","Mipmap","",2),
            ("linearMipNN","Linear, Mip Nearest Neighbour","Mipmap Bilinear","",3),
            ("linearMipL","Linear, Mip Linear","Mipmap Trilinear","",4)
        ],
        default=1
    )
    uvMode: bpy.props.EnumProperty(
        name="UV Mode",
        items=[
            ("tile","Tile","","",0),
            ("clamp","Clamp","","",1),
        ]
    )
    lighting: bpy.props.BoolProperty(
        name="Lighting",
        default=False
    )
    alphaTest: bpy.props.BoolProperty(
        name="Alpha Test",
        default=False,
        update=update_shader_properties
    )
    twoSided: bpy.props.BoolProperty(
        name="Two Sided",
        default=False,
        update=update_shader_properties
    )
    shininess: bpy.props.FloatProperty(
        name="Shininess",
        min=0,
        max=200,
        default=10
    )
    alphaCompare: bpy.props.EnumProperty(
        name="Alpha Compare",
        items=[
            ("none","None","","",0),
            ("always","Always","","",1),
            ("less","Less","","",2),
            ("lessEqual","LessEqual","","",3),
            ("greater","Greater","","",4),
            ("greaterEqual","GreaterEqual","","",5),
            ("equal","Equal","","",6),
            ("notEqual","NotEqual","","",7),
        ],
        default=4
    )
    alphaCompareThreshold: bpy.props.FloatProperty(
        name="Alpha Compare Threshold",
        min=0,
        max=1,
        default=0.5,
        description="The alpha threshold used by the Alpha-Compare test"
    )
    shadeMode: bpy.props.EnumProperty(
        name="Shade Mode",
        items=[
            ("flat","Flat","","",0),
            ("gouraud","Gouraud","","",1),
        ],
        default=1
    )
    mipmapMin: bpy.props.EnumProperty(
        name="Mipmap Min",
        items=[
            ("8","8","","",0),
            ("16","16","","",1),
            ("32","32","","",2),
            ("64","64","","",3),
            ("128","128","","",4),
            ("256","256","","",5),
            ("512","512","","",6),
            ("1024","1024","","",7),
        ],
        default=0,
        description="Minimum dimension of the mipmapped texture"
    )
    mipmapMax: bpy.props.EnumProperty(
        name="Mipmap Max",
        items=[
            ("8","8","","",0),
            ("16","16","","",1),
            ("32","32","","",2),
            ("64","64","","",3),
            ("128","128","","",4),
            ("256","256","","",5),
            ("512","512","","",6),
            ("1024","1024","","",7),
        ],
        default=7,
        description="Maximum dimension of the mipmapped texture"
    )
    rawTextureName: bpy.props.StringProperty(
        name="Raw Texture Name",
        description="Texture name to be used when no image is set",
        default=""
    )
    terrainType: bpy.props.EnumProperty(
        name = "Terrain Type",
        description="Terrain Type, used when generating intersects",
        items = [
            ("unset","Unset",""),
            ("0","Road","Default road terrain. Also used for sidewalk"),
            ("1","Grass","Grass type terrain most everything else which isn't road or sidewalk"),
            ("2","Sand","Sand type terrain"),
            ("3","Gravel","Loose gravel type terrain"),
            ("4","Water","Water on surface type terrain"),
            ("5","Wood","Boardwalks, docks type terrain"),
            ("6","Metal","Powerplant and other structures"),
            ("7","Dirt","Dirt type terrain"),
        ],
        default = "unset"
    )

class ShaderPropertiesPanel(bpy.types.Panel):
    bl_label = "SHAR Shader Properties"
    bl_idname = "OBJECT_PT_shar_shader_properties"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"

    @classmethod
    def poll(self,context):
        return context.material is not None

    def draw(self, context):
        layout = self.layout

        mat = context.material

        if mat is None:
            return

        # Fix spacing
        layout.use_property_split = True
        layout.use_property_decorate = False

        # Props
        layout.prop(mat,"name")
        layout.prop(mat.shaderProperties,"pddiShader")
        if mat.use_nodes and mat.node_tree is not None and "Principled BSDF" in mat.node_tree.nodes and "Image Texture" in mat.node_tree.nodes and mat.node_tree.nodes["Image Texture"].image is not None:
            layout.label(text="Change texture above")
        else:
            layout.label(text="Add image texture above or:")
            layout.prop(mat.shaderProperties,"rawTextureName")
        layout.prop(mat.shaderProperties,"diffuseColor")
        layout.prop(mat.shaderProperties,"specularColor")
        layout.prop(mat.shaderProperties,"ambientColor")
        layout.label(text="Change emission above")
        layout.prop(mat.shaderProperties,"blendMode")
        layout.prop(mat.shaderProperties,"filterMode")
        layout.prop(mat.shaderProperties,"uvMode")
        layout.prop(mat.shaderProperties,"lighting")
        layout.prop(mat.shaderProperties,"alphaTest")
        layout.prop(mat.shaderProperties,"twoSided")
        layout.prop(mat.shaderProperties,"shininess")
        layout.prop(mat.shaderProperties,"terrainType")
        panel_header, panel_body = layout.panel("shaderPropertiesAdvanced",default_closed=True)
        panel_header.label(text="Advanced")
        if panel_body is not None:
            layout.prop(mat.shaderProperties,"shadeMode")
            layout.prop(mat.shaderProperties,"alphaCompare")
            layout.prop(mat.shaderProperties,"alphaCompareThreshold")
            layout.prop(mat.shaderProperties,"mipmapMin")
            layout.prop(mat.shaderProperties,"mipmapMax")
        

def register():
    bpy.utils.register_class(ShaderProperties)

    bpy.types.Material.shaderProperties = bpy.props.PointerProperty(type=ShaderProperties)

    bpy.utils.register_class(ShaderPropertiesPanel)

def unregister():
    bpy.utils.unregister_class(ShaderProperties)

    bpy.utils.unregister_class(ShaderPropertiesPanel)