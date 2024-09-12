#
# Imports
#

import bpy

#
# Class
#

class PURE3D_FH(bpy.types.FileHandler):
    bl_idname = "PURE3D_FH_importexport"
    bl_label = "Pure3D"
    bl_import_operator = "operators.raw_import_pure3d_file"
    bl_export_operator = "operators.raw_export_pure3d_file"
    bl_file_extensions = ".p3d"

    @classmethod
    def poll_drop(cls, context):
        return (context.area and context.area.type == 'VIEW_3D')

def register():
    bpy.utils.register_class(PURE3D_FH)

def unregister():
    bpy.utils.unregister_class(PURE3D_FH)