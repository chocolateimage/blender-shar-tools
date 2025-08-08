import bpy

#
# Utility Functions
#

def alert(message = "", title = "SHAR Blender Tools", icon = "INFO"):
    def draw(self, context):
        lines = message.split("\n")

        for line in lines:
            self.layout.label(text = line)

    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)