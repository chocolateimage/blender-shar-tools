#
# Imports
#

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
        utils.layout_wrapped_label(layout,context,"P3D files are collections stored in the scene")
        layout.operator(OBJECT_OT_sharmanagment_add_p3d.bl_idname)

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
        fileCollection.children.link(bpy.data.collections.new("Static Entities"))
        fileCollection.children.link(bpy.data.collections.new("Collision"))
        fileCollection.children.link(bpy.data.collections.new("Instanced"))


        return {"FINISHED"}

def register():
    bpy.utils.register_class(OBJECT_OT_sharmanagment_add_p3d)
    bpy.utils.register_class(OBJECT_PT_sharmanagement_panel)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_sharmanagment_add_p3d)
    bpy.utils.unregister_class(OBJECT_PT_sharmanagement_panel)