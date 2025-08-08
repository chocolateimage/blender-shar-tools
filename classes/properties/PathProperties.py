import bpy

#
# Class
#

class OBJECT_PT_path_panel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_path_panel"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SHAR Blender Tools"
    bl_label = "Paths"

    def draw(self, context):
        layout = self.layout

        if context.object and context.object.isPath:
            # TODO: Add a button to flip the path
            pass

def register():
    bpy.types.Object.isPath = bpy.props.BoolProperty(name = "Is Path", default = False)

    bpy.utils.register_class(OBJECT_PT_path_panel)

def unregister():
    del bpy.types.Object.isPath

    bpy.utils.unregister_class(OBJECT_PT_path_panel)