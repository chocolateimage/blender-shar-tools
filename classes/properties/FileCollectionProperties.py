import bpy
import mathutils

#
# Class
#

class StickyImage(bpy.types.PropertyGroup):
    image: bpy.props.PointerProperty(
        type = bpy.types.Image,
        name = "Image"
    )

class StickyImagesAddOperator(bpy.types.Operator):
    bl_idname="collection.shar_stickyimage_add"
    bl_label="Add sticky image"

    def execute(self, context):
        context.collection.fileCollectionProperties.sharStickyImages.add()
        context.collection.fileCollectionProperties.sharStickyImagesId = len(context.collection.fileCollectionProperties.sharStickyImages) - 1
        return {"FINISHED"}

class StickyImagesRemoveOperator(bpy.types.Operator):
    bl_idname="collection.shar_stickyimage_remove"
    bl_label="Remove sticky image"

    index: bpy.props.IntProperty()

    def execute(self, context):
        context.collection.fileCollectionProperties.sharStickyImages.remove(self.index)
        return {"FINISHED"}

class SHAR_UL_Sticky_Images(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout: bpy.types.UILayout = layout
        row = layout.row(align=True)
        row.prop(item, "image", text="")
        removeOperator = row.operator(StickyImagesRemoveOperator.bl_idname, icon="REMOVE", text="")
        removeOperator.index = index

class FileCollectionProperties(bpy.types.PropertyGroup):
    sharStickyImages: bpy.props.CollectionProperty(type = StickyImage)
    sharStickyImagesId: bpy.props.IntProperty(default=0)

class FileCollectionPanel(bpy.types.Panel):
    bl_label = "SHAR Pure3D File Properties"
    bl_idname = "OBJECT_PT_shar_p3d_file_properties"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "collection"

    @classmethod
    def poll(self,context):
        return context.collection and context.collection.name.endswith(".p3d")
    
    def draw(self, context):
        layout = self.layout

        collection = context.collection

        if collection is None:
            return

        # Fix spacing
        layout.use_property_split = True
        layout.use_property_decorate = False

        # Props
        fileCollectionProperties = collection.fileCollectionProperties
        
        layout.label(text="Sticky Images")

        row = layout.row()
        row.template_list("SHAR_UL_Sticky_Images", "sticky_images", fileCollectionProperties, "sharStickyImages", fileCollectionProperties, "sharStickyImagesId")

        col = row.column()
        col.operator(StickyImagesAddOperator.bl_idname, icon="ADD", text="")
        

def register():
    bpy.utils.register_class(StickyImage)
    bpy.utils.register_class(SHAR_UL_Sticky_Images)
    bpy.utils.register_class(StickyImagesAddOperator)
    bpy.utils.register_class(StickyImagesRemoveOperator)

    bpy.utils.register_class(FileCollectionPanel)
    bpy.utils.register_class(FileCollectionProperties)

    bpy.types.Collection.fileCollectionProperties = bpy.props.PointerProperty(type = FileCollectionProperties)


def unregister():
    del bpy.types.Collection.fileCollectionProperties

    bpy.utils.unregister_class(StickyImage)
    bpy.utils.unregister_class(SHAR_UL_Sticky_Images)
    bpy.utils.unregister_class(StickyImagesAddOperator)
    bpy.utils.unregister_class(StickyImagesRemoveOperator)

    bpy.utils.unregister_class(FileCollectionPanel)
    bpy.utils.unregister_class(FileCollectionProperties)


