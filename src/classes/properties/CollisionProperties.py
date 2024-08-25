#
# Imports
#

import bpy
import mathutils
import utils

#
# Class
#

def update_collision_properties(self,context):
	obj: bpy.types.Object = getattr(self,"id_data",None)
	
	mesh: bpy.types.Mesh = obj.data

	if obj.collisionProperties.collisionType == "Cylinder":
		for i in mesh.polygons:
			i.use_smooth = not obj.collisionProperties.flatEnd
		
		obj.scale = mathutils.Vector((1,1,1))
		
		originalcoords = obj.collisionProperties.originalCoords.split("|")
		for i,v in enumerate(mesh.vertices):
			original = originalcoords[i].split(",")
			newx = float(original[0])
			newy = float(original[1])
			newz = float(original[2])

			newx *= obj.collisionProperties.radius
			newy *= obj.collisionProperties.radius
			newz *= obj.collisionProperties.radius
			if newz < 0:
				if obj.collisionProperties.flatEnd:
					newz = 0
				newz -= obj.collisionProperties.length
			if newz > 0:
				if obj.collisionProperties.flatEnd:
					newz = 0
				newz += obj.collisionProperties.length

			v.co.x = newx
			v.co.y = newy
			v.co.z = newz
	
	if obj.collisionProperties.collisionType == "Sphere":
		for i in mesh.polygons:
			i.use_smooth = True

		originalcoords = obj.collisionProperties.originalCoords.split("|")
		for i,v in enumerate(mesh.vertices):
			original = originalcoords[i].split(",")
			newx = float(original[0])
			newy = float(original[1])
			newz = float(original[2])

			newx *= obj.collisionProperties.radius
			newy *= obj.collisionProperties.radius
			newz *= obj.collisionProperties.radius

			v.co.x = newx
			v.co.y = newy
			v.co.z = newz


class CollisionProperties(bpy.types.PropertyGroup):
	collisionType: bpy.props.StringProperty(
		name="Collision Type",
		default="" # Empty string means isn't a collision
	)
	radius: bpy.props.FloatProperty(
		name="Radius",
		update=update_collision_properties
	)
	length: bpy.props.FloatProperty(
		name="Length",
		update=update_collision_properties
	)
	flatEnd: bpy.props.BoolProperty(
		name="Flat End",
		default=False,
		update=update_collision_properties
	)
	originalCoords: bpy.props.StringProperty()
	hasCollisionEffect: bpy.props.BoolProperty(
		default=False
	)
	collisionEffectClassType: bpy.props.EnumProperty(
		name = "Class Type",
		items = [
			("0","WTF","","",0),
			("1","Ground","","",1),
			("2","Prop Static","","",2),
			("3","Prop Moveable","","",3),
			("4","Prop Breakable","","",4),
			("5","Animated BV","","",5),
			("6","Drawable","","",6),
			("7","Static","","",7),
			("8","Prop Drawable","","",8),
			("9","Prop Anim Breakable","","",9),
			("10","Prop Onetime Moveable","","",10)
		],
		default = 7
	)
	collisionEffectPhyPropID: bpy.props.EnumProperty(
		name = "Phys Prop ID",
		description = "List shown was generated from art/atc/atc.p3d\nalso known as \"PhyPropID\" and \"ATC\"\nSound, Particle, BreakableObject",
		items = [
			("0","WTF, WTF, WTF","","",0),
			("1","smash, Not set, Not set","","",1),
			("2","smash, Not set, eHydrantBreaking","","",2),
			("3","smash, eSpark, Not set","","",3),
			("4","smash, Not set, Not set","","",4),
			("5","smash, Not set, Not set","","",5),
			("6","car_hit_hydrant, Not set, Not set","","",6),
			("7","smash, Not set, Not set","","",7),
			("8","smash, eGarbage, Not set","","",8),
			("9","smash, eNull, eOakTreeBreaking","","",9),
			("10","smash, eShrub, Not set","","",10),
			("11","large_car_crash, eOakTreeLeaves, Not set","","",11),
			("12","car_hit_tree, eMail, Not set","","",12),
			("13","smash, eSpark, Not set","","",13),
			("14","smash, Not set, ePineTreeBreaking","","",14),
			("15","smash, eStars, Not set","","",15),
			("16","smash, eNull, eRailCrossBreaking","","",16),
			("17","smash, eNull, eBigBarrierBreaking","","",17),
			("18","smash, eNull, Not set","","",18),
			("19","smash, eSpark, Not set","","",19),
			("20","smash, Not set, Not set","","",20),
			("21","smash, eStars, Not set","","",21),
			("22","smash, eMail, Not set","","",22),
			("23","smash, eStars, eStopsign","","",23),
			("24","smash, eSpark, Not set","","",24),
			("25","smash, eStars, Not set","","",25),
			("26","smash, eNull, eTomaccoBreaking","","",26),
			("27","smash, eSpark, Not set","","",27),
			("28","smash, eNull, Not set","","",28),
			("29","smash, eGarbage, Not set","","",29),
			("30","smash, eSpark, Not set","","",30),
			("31","smash, eParkingMeter, Not set","","",31),
			("32","smash, eCoconutsDroppingShort, ePalmTreeSmall","","",32),
			("33","smash, eNull, Not set","","",33),
			("34","smash, eNull, Not set","","",34),
			("35","smash, eNull, Not set","","",35),
			("36","smash, eNull, Not set","","",36),
			("37","smash, eNull, Not set","","",37),
			("38","smash, eNull, Not set","","",38),
			("39","smash, eSpark, Not set","","",39),
			("40","smash, eStars, Not set","","",40),
			("41","smash, eSpark, Not set","","",41),
			("42","smash, eStars, eWillow","","",42),
			("43","smash, eNull, Not set","","",43),
			("44","smash, eNull, eKrustyGlassBreaking","","",44),
			("45","smash, eNull, eSpaceNeedleBreaking","","",45),
			("46","smash, eNull, Not set","","",46),
			("47","smash, eNull, eCypressTreeBreaking","","",47),
			("48","smash, eNull, eDeadTreeBreaking","","",48),
			("49","smash, Not set, eSkeletonBreaking","","",49),
			("50","smash, eCoconutsDroppingTall, ePalmTreeLarge","","",50),
			("51","large_car_crash, Not set, Not set","","",51),
			("52","smash, eNull, Not set","","",52),
			("53","smash, ePopsicles, Not set","","",53),
			("54","smash, Not set, eSkeletonBreaking","","",54),
			("55","smash, eNull, eGlobeLight","","",55),
			("56","smash, eNull, ePalmTreeLarge","","",56),
			("57","smash, eNull, eTreeMorn","","",57),
			("58","smash, eNull, Not set","","",58),
			("59","smash, eNull, ePumpkin","","",59),
			("60","smash, eNull, ePumpkinMed","","",60),
			("61","smash, eNull, ePumpkinSmall","","",61),
			("62","smash, eNull, eCasinoJump","","",62),
		],
		default = 0
	)
	collisionEffectSound: bpy.props.StringProperty(
		name = "Sound",
		default = "nosound"
	)
	physicsRestingSensitivity: bpy.props.FloatProperty(
		name = "Resting Sensitivity",
		default = 1
	)
	physicsVolume: bpy.props.FloatProperty(
		name = "Volume",
		default = 1
	)

class CollisionPropertiesPanel(bpy.types.Panel):
	bl_idname = "OBJECT_PT_shar_collision_properties"

	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "SHAR Blender Tools"
	bl_label = "Collision"

	def draw(self, context):
		layout = self.layout

		obj = context.object

		if obj and obj.collisionProperties and obj.collisionProperties.collisionType != "":
			layout.label(text=obj.collisionProperties.collisionType)
			if obj.collisionProperties.collisionType == "Box":
				layout.prop(obj,"scale")
			elif obj.collisionProperties.collisionType == "Cylinder":
				layout.prop(obj.collisionProperties,"radius")
				layout.prop(obj.collisionProperties,"length")
				layout.prop(obj.collisionProperties,"flatEnd")
			elif obj.collisionProperties.collisionType == "Sphere":
				layout.prop(obj.collisionProperties,"radius")
			layout.separator()

			basename = utils.get_basename(obj.name)
			original_objects = []
			for collection in obj.users_collection:
				for other_object in collection.objects:
					other_object_basename = utils.get_basename(other_object.name)
					if other_object_basename != basename:
						continue
					if other_object.collisionProperties and other_object.collisionProperties.collisionType != "" and other_object.collisionProperties.hasCollisionEffect:
						original_objects.append(other_object)
			
			layout.label(text="Settings for " + basename)
			if len(original_objects) == 1:
				original_object = original_objects[0]
				layout.prop(original_object.collisionProperties,"collisionEffectClassType")
				layout.prop(original_object.collisionProperties,"collisionEffectPhyPropID")
				layout.prop(original_object.collisionProperties,"collisionEffectSound")
				if int(original_object.collisionProperties.collisionEffectClassType) in [3, 4, 10]:
					layout.prop(original_object.collisionProperties,"physicsRestingSensitivity")
					layout.prop(original_object.collisionProperties,"physicsVolume")
				layout.label(text="Stored in object " + original_object.name)
			elif len(original_objects) > 1:
				layout.label(text="Multiple objects with collision effect! Only one per group allowed.",icon="ERROR")
				for i in original_objects:
					keepOperator = layout.operator(OBJECT_OT_keep_shar_collision_effect.bl_idname, text="Keep " + i.name)
					keepOperator.keepObjectName = i.name
			else:
				layout.operator(OBJECT_OT_add_shar_collision_effect.bl_idname)

class OBJECT_OT_add_shar_collision_effect(bpy.types.Operator):
	bl_idname = "object.add_shar_collision_effect"
	bl_label = "Add Collision Effect"
	bl_options = {"REGISTER", "UNDO"}
	
	def execute(self, context):
		obj = context.object
		
		obj.collisionProperties.hasCollisionEffect = True

		return {"FINISHED"}

class OBJECT_OT_keep_shar_collision_effect(bpy.types.Operator):
	bl_idname = "object.keep_shar_collision_effect"
	bl_label = "Keep Collision Effect"
	bl_options = {"REGISTER", "UNDO"}

	keepObjectName: bpy.props.StringProperty()
	
	def execute(self, context):
		obj = bpy.data.objects[self.keepObjectName]
		
		obj.collisionProperties.hasCollisionEffect = True
		basename = utils.get_basename(obj.name)
		for collection in obj.users_collection:
			for other_object in collection.objects:
				if other_object == obj:
					continue
				other_object_basename = utils.get_basename(other_object.name)
				if other_object_basename != basename:
					continue
				other_object.collisionProperties.hasCollisionEffect = False

		return {"FINISHED"}

def register():
	bpy.utils.register_class(CollisionProperties)

	bpy.types.Object.collisionProperties = bpy.props.PointerProperty(type=CollisionProperties)

	bpy.utils.register_class(CollisionPropertiesPanel)

	bpy.utils.register_class(OBJECT_OT_add_shar_collision_effect)

	bpy.utils.register_class(OBJECT_OT_keep_shar_collision_effect)

def unregister():
	bpy.utils.unregister_class(OBJECT_OT_keep_shar_collision_effect)

	bpy.utils.unregister_class(OBJECT_OT_add_shar_collision_effect)

	bpy.utils.unregister_class(CollisionPropertiesPanel)

	bpy.utils.unregister_class(CollisionProperties)

	del bpy.types.Object.collisionProperties