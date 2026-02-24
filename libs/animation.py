import bpy

from classes.chunks.AnimationChunk import AnimationChunk
from classes.chunks.AnimationGroupChunk import AnimationGroupChunk
from classes.chunks.AnimationGroupListChunk import AnimationGroupListChunk
from classes.chunks.CompressedQuaternionChannelChunk import CompressedQuaternionChannelChunk
from classes.chunks.QuaternionChannelChunk import QuaternionChannelChunk
from classes.chunks.Vector1DOFChannelChunk import Vector1DOFChannelChunk
from classes.chunks.Vector2DOFChannelChunk import Vector2DOFChannelChunk
from classes.chunks.Vector3DOFChannelChunk import Vector3DOFChannelChunk
from data.matrices import MATRIX_SWAP

def createAnimation(animationChunk: AnimationChunk):
    scene = bpy.context.scene
    frameMultiplier = scene.render.fps / animationChunk.frameRate

    actions: list[bpy.types.Action] = []

    groupList = animationChunk.getFirstChildOfType(AnimationGroupListChunk)
    for group in groupList.getChildrenOfType(AnimationGroupChunk):
        actionName = f"{animationChunk.name}.{group.name}"

        action: bpy.types.Action = bpy.data.actions.new(actionName)

        action.frame_end = animationChunk.numberOfFrames

        slot = action.slots.new("OBJECT", actionName)
        layer: bpy.types.ActionLayer = action.layers.new("default")
        strip: bpy.types.ActionKeyframeStrip = layer.strips.new(type="KEYFRAME")

        for channel in group.children:
            param = getattr(channel, "param", None)
            dataPath = None
            if param == "TRAN":
                dataPath = "location"
            elif param == "ROT":
                dataPath = "rotation_quaternion"
            else:
                print(f"Unknown animation param {param}")
                continue

            if type(channel) is Vector3DOFChannelChunk:
                for frame, value in zip(channel.frames, channel.values):
                    strip.key_insert(slot, dataPath, 0, value.x, frame * frameMultiplier)
                    strip.key_insert(slot, dataPath, 1, value.z, frame * frameMultiplier)
                    strip.key_insert(slot, dataPath, 2, value.y, frame * frameMultiplier)
            elif type(channel) is Vector1DOFChannelChunk:
                vector = channel.constants.copy()
                for frame, value in zip(channel.frames, channel.values):
                    vector[channel.mapping] = value
                    strip.key_insert(slot, dataPath, 0, vector.x, frame * frameMultiplier)
                    strip.key_insert(slot, dataPath, 1, vector.z, frame * frameMultiplier)
                    strip.key_insert(slot, dataPath, 2, vector.y, frame * frameMultiplier)
            elif type(channel) is Vector2DOFChannelChunk:
                vector = channel.constants.copy()
                indicies = ((1,2),(0,2),(0,1))[channel.mapping]
                for frame, value in zip(channel.frames, channel.values):
                    vector[indicies[0]] = value.x
                    vector[indicies[1]] = value.y
                    strip.key_insert(slot, dataPath, 0, vector.x, frame * frameMultiplier)
                    strip.key_insert(slot, dataPath, 1, vector.z, frame * frameMultiplier)
                    strip.key_insert(slot, dataPath, 2, vector.y, frame * frameMultiplier)
            elif type(channel) is QuaternionChannelChunk or type(channel) is CompressedQuaternionChannelChunk:
                for frame, value in zip(channel.frames, channel.values):
                    matrix = value.to_matrix().to_4x4()
                    matrix = MATRIX_SWAP @ matrix @ MATRIX_SWAP.inverted()
                    quat = matrix.to_quaternion()
                    strip.key_insert(slot, dataPath, 0, quat.w, frame * frameMultiplier)
                    strip.key_insert(slot, dataPath, 1, quat.x, frame * frameMultiplier)
                    strip.key_insert(slot, dataPath, 2, quat.y, frame * frameMultiplier)
                    strip.key_insert(slot, dataPath, 3, quat.z, frame * frameMultiplier)
            else:
                print(f"Unknown channel type in {group.name}")
        
        for channelbag in strip.channelbags:
            channelbag: bpy.types.ActionChannelbag
            for fcurve in channelbag.fcurves:
                fcurve: bpy.types.FCurve
                for keyframePoint in fcurve.keyframe_points:
                    keyframePoint: bpy.types.Keyframe
                    keyframePoint.interpolation = "LINEAR"

    return actions
