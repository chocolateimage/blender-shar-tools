#
# Import
#

import bpy
import re
import mathutils
import math

import libs.collision as CollisionLib

#
# Operators
#

def collisionGroupSearch(self, context, edit_text):
    items = []
    query = edit_text.lower()
    for collection in bpy.data.collections:
        collectionBasename = re.sub(r"\.\d+$", "", collection.name)
        if collectionBasename == "Collisions":
            for obj in collection.objects:
                objectBasename = re.sub(r"\.\d+$", "", obj.name)
                if query in objectBasename.lower():
                    if objectBasename not in items:
                        items.append(objectBasename)
    items.sort()

    return items

class BaseCollisionOperator(bpy.types.Operator):
    group: bpy.props.StringProperty(
        name="Group",
        search=collisionGroupSearch
    )

    def execute(self,context,obj):
        if self.group in bpy.data.objects:
            for collection in obj.users_collection:
                collection.objects.unlink(obj)
            for collection in bpy.data.objects[self.group].users_collection:
                collection.objects.link(obj)
        else:
            bpy.context.collection.objects.link(obj)
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        if self.group == "":
            obj.name = "Unnamed collision"
        else:
            obj.name = self.group
        return {"FINISHED"}

    def draw(self,context):
        layout = self.layout

        layout.separator()
        layout.column().prop(self,"group")
        is_in_collisions_collection = False
        for collection in context.active_object.users_collection:
            collectionBasename = re.sub(r"\.\d+$", "", collection.name)
            if collectionBasename == "Collisions":
                is_in_collisions_collection = True

        if not is_in_collisions_collection:
            layout.alert = True
            layout.label(text="Object is not in a collision collection", icon="ERROR")
            layout.alert = False
        
        layout.separator()
        layout.use_property_split = False
        col = layout.column()
        col.scale_y = 0.7
        col.label(text="You can change all settings later in the SHAR")
        col.label(text="Tools panel")

class OBJECT_OT_add_shar_collision_box(BaseCollisionOperator):
    bl_idname = "object.add_shar_collision_box"
    bl_label = "Add Collision Box"
    bl_description = "Add a collision box"
    bl_options = {"REGISTER", "UNDO"}
    
    location: bpy.props.FloatVectorProperty(
        name="Location"
    )
    rotation: bpy.props.FloatVectorProperty(
        name="Rotation"
    )
    size: bpy.props.FloatVectorProperty(
        name="Size",
        default=(1,1,1)
    )

    def execute(self, context):
        obj = CollisionLib.createNewCollisionBox()
        obj.location = self.location
        obj.rotation_euler = mathutils.Vector(self.rotation) * math.pi / 180
        obj.scale = self.size
        return super().execute(context,obj)
    
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        layout.column().prop(self,"location")
        layout.column().prop(self,"rotation")
        layout.column().prop(self,"size")

        return super().draw(context)

class OBJECT_OT_add_shar_collision_cylinder(BaseCollisionOperator):
    bl_idname = "object.add_shar_collision_cylinder"
    bl_label = "Add Collision Cylinder"
    bl_description = "Add a collision cylinder"
    bl_options = {"REGISTER", "UNDO"}
    
    location: bpy.props.FloatVectorProperty(
        name="Location"
    )
    rotation: bpy.props.FloatVectorProperty(
        name="Rotation"
    )
    radius: bpy.props.FloatProperty(
        name="Radius",
        default=1
    )
    length: bpy.props.FloatProperty(
        name="Length",
        default=1
    )
    flatEnd: bpy.props.BoolProperty(
        name="Flat End",
        description="Disabled: Round end\nEnabled: Flat end"
    )

    def execute(self, context):
        obj = CollisionLib.createNewCollisionCylinder(self.radius,self.length,self.flatEnd)
        obj.location = self.location
        obj.rotation_euler = mathutils.Vector(self.rotation) * math.pi / 180
        return super().execute(context,obj)
    
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        layout.column().prop(self,"location")
        layout.column().prop(self,"rotation")
        layout.column().prop(self,"radius")
        layout.column().prop(self,"length")
        layout.column().prop(self,"flatEnd")

        return super().draw(context)

class OBJECT_OT_add_shar_collision_sphere(BaseCollisionOperator):
    bl_idname = "object.add_shar_collision_sphere"
    bl_label = "Add Collision Sphere"
    bl_description = "Add a collision sphere"
    bl_options = {"REGISTER", "UNDO"}
    
    location: bpy.props.FloatVectorProperty(
        name="Location"
    )
    radius: bpy.props.FloatProperty(
        name="Radius",
        default=1
    )

    def execute(self, context):
        obj = CollisionLib.createNewCollisionSphere(self.radius)
        obj.location = self.location
        return super().execute(context,obj)
    
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        layout.column().prop(self,"location")
        layout.column().prop(self,"radius")

        return super().draw(context)

class VIEW3D_MT_shar_collision_menu(bpy.types.Menu):
    bl_idname = "VIEW3D_MT_shar_collision_menu"
    bl_label = "SHAR Collision"

    def draw(self, context):
        layout = self.layout
        layout.operator(OBJECT_OT_add_shar_collision_box.bl_idname, text="Box", icon="CUBE")
        layout.operator(OBJECT_OT_add_shar_collision_cylinder.bl_idname, text="Cylinder", icon="MESH_CYLINDER")
        layout.operator(OBJECT_OT_add_shar_collision_sphere.bl_idname, text="Sphere", icon="SPHERE")


def draw_custom_menu(self, context):
    layout = self.layout
    layout.menu(VIEW3D_MT_shar_collision_menu.bl_idname, icon="MOD_PHYSICS")

def register():
    bpy.utils.register_class(VIEW3D_MT_shar_collision_menu)
    bpy.utils.register_class(OBJECT_OT_add_shar_collision_box)
    bpy.utils.register_class(OBJECT_OT_add_shar_collision_cylinder)
    bpy.utils.register_class(OBJECT_OT_add_shar_collision_sphere)

    bpy.types.VIEW3D_MT_add.append(draw_custom_menu)

def unregister():
    bpy.utils.unregister_class(VIEW3D_MT_shar_collision_menu)
    bpy.utils.unregister_class(OBJECT_OT_add_shar_collision_box)
    bpy.utils.unregister_class(OBJECT_OT_add_shar_collision_cylinder)
    bpy.utils.unregister_class(OBJECT_OT_add_shar_collision_sphere)

    bpy.types.VIEW3D_MT_add.remove(draw_custom_menu)