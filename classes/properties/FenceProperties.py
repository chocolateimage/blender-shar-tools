#
# Imports
#

import bpy

#
# Class
#

class FenceProperties(bpy.types.PropertyGroup):
    isFlipped: bpy.props.BoolProperty(name = "Is Flipped", default = False)

class OBJECT_PT_fence_panel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_fence_panel"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SHAR Blender Tools"
    bl_label = "Fences"

    def draw(self, context):
        layout = self.layout

        if context.object and context.object.isFence:
            # https://docs.blender.org/api/current/bpy.types.UILayout.html#bpy.types.UILayout.prop
            layout.prop(context.object.fenceProperties, "isFlipped")

            # TODO: Flip the spline points when checking/unchecking this property
            # TODO: Maybe don't actually show the property and have a button to flip the spline points instead?
            #        Still uses the property, but it's not directly visible to the user

def register():
    bpy.utils.register_class(FenceProperties)

    bpy.types.Object.isFence = bpy.props.BoolProperty(name = "Is Fence", default = False)
    bpy.types.Object.fenceProperties = bpy.props.PointerProperty(type = FenceProperties)

    bpy.utils.register_class(OBJECT_PT_fence_panel)

def unregister():
    bpy.utils.unregister_class(FenceProperties)

    del bpy.types.Object.isFence
    del bpy.types.Object.fenceProperties

    bpy.utils.unregister_class(OBJECT_PT_fence_panel)