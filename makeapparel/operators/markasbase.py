#!/usr/bin/python
# -*- coding: utf-8 -*-

import bpy

def getMeshType(baseObj):
    for group in baseObj.vertex_groups:
        if group.name.startswith('_mesh_'):
            return group.name[6:]
    if hasattr(baseObj, "MhMeshType") and baseObj.MhMeshType != "":
        return baseObj.MhMeshType
    return "hm08"

#
# we need this when we import a base mesh, it will be marked automatically
#
def markAsBase(context):

    #
    # unmark existent mesh if not the same (it helps when you work with
    # a lot of assets and accidentally mark an object as a base
    #
    unmarked = ""
    for obj in context.scene.objects:
        if obj != context.active_object and hasattr(obj, "MhObjectType"):
            if obj.MhObjectType == "Basemesh":
                unmarked += obj.name + " "
                obj.MhObjectType = "Clothes"

    context.active_object.MhObjectType = "Basemesh"
    context.active_object.MhMeshType = getMeshType(context.active_object)
    if unmarked != "":
        text = "Marks change to clothes for: " + unmarked + ". Selected object marked as base, mesh type is " + context.active_object.MhMeshType
    else:
        text = "Selected object marked as base, mesh type is " + context.active_object.MhMeshType
    return (text)

class MHC_OT_MarkAsBaseOperator(bpy.types.Operator):
    """Mark this object to be used as basemesh"""
    bl_idname = "makeapparel.mark_as_base"
    bl_label = "Mark selected object as base"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        return context.active_object is not None and context.active_object.type == 'MESH'

    def getMeshType(self, baseObj):
        for group in baseObj.vertex_groups:
            if group.name.startswith('_mesh_'):
                return group.name[6:]
        return "hm08"

    def execute(self, context):
        text = markAsBase(context)
        self.report({'INFO'}, text)
        return {'FINISHED'}
