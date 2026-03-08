import bpy
import utils

#
# Class
#

class OBJECT_PT_sharmanagement_panel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_sharmanagement_panel"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SHAR Blender Tools"
    bl_label = "Management"

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        utils.layout_wrapped_label(box, context, "P3D files are collections stored in the scene")
        box.operator(OBJECT_OT_sharmanagment_add_p3d.bl_idname)

        self.draw_object(context)

    def draw_object(self, context: bpy.types.Context):
        object = context.object
        if object is None:
            return

        p3d_collection = utils.find_p3d_collection_from_object(object)

        if p3d_collection is None:
            return
        
        export_as = None
        icon = "OBJECT_DATA"

        if len(object.users_collection) != 1:
            utils.layout_wrapped_label(self.layout, context, "Selected object can only be in one collection at a time")
            return

        object_collection = object.users_collection[0]
        if utils.get_basename(object_collection.name) == "Terrain":
            if utils.get_basename(object.name).endswith("_COL"):
                export_as = "StaticPhys"
                icon = {"Box": "CUBE", "Cylinder": "MESH_CYLINDER", "Sphere": "SPHERE"}.get(object.collisionProperties.collisionType, "QUESTION")

            else:
                export_as = "StaticEntity"

        if export_as is None:
            return

        box = self.layout.box()
        box.label(text=object.name, icon=icon)
        box.label(text=f"Will export as: {export_as}")

class OBJECT_OT_sharmanagment_add_p3d(bpy.types.Operator):
    bl_idname = "object.sharmanagement_add_p3d"
    bl_label = "Add P3D"
    bl_options = {"UNDO"}
    
    def execute(self, context):
        name_num = 1
        name = ""
        while True:
            name = "Untitled P3D File"
            if name_num > 1:
                name += " " + str(name_num)
            name += ".p3d"
            if name in bpy.data.collections:
                name_num += 1
            else:
                break
        
        
    
        fileCollection = bpy.data.collections.new(name)

        bpy.context.scene.collection.children.link(fileCollection)

        fileCollection.children.link(bpy.data.collections.new("Fences"))
        fileCollection.children.link(bpy.data.collections.new("Paths"))
        fileCollection.children.link(bpy.data.collections.new("Terrain"))
        fileCollection.children.link(bpy.data.collections.new("Entities"))


        return {"FINISHED"}

def register():
    bpy.utils.register_class(OBJECT_OT_sharmanagment_add_p3d)
    bpy.utils.register_class(OBJECT_PT_sharmanagement_panel)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_sharmanagment_add_p3d)
    bpy.utils.unregister_class(OBJECT_PT_sharmanagement_panel)