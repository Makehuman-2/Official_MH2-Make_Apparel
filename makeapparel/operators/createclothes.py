#!/usr/bin/python
# -*- coding: utf-8 -*-

import bpy
import os
from ..sanitychecks import checkSanityBase, checkSanityClothes
from ..core_functionality import MakeApparel
from ..utils import getClothesRoot

class MHC_OT_CreateClothesOperator(bpy.types.Operator):
    """Produce MHCLO file and MHMAT, copy textures"""
    bl_idname = "makeapparel.create_clothes"
    bl_label = "Create clothes"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(self, context):
        if context.active_object is not None:
            if not hasattr(context.active_object, "MhObjectType"):
                return False
            if context.active_object.select_get():
                if context.active_object.MhObjectType == "Clothes":
                    return True
        return False

    def execute(self, context):

        (b, info, error) = checkSanityBase(context)
        if b:
            bpy.ops.makeapparel.infobox('INVOKE_DEFAULT', title="Check Base", info=info, error=error)
            return {'FINISHED'}

        # since we tested the existence of a base above there is exactly one
        #
        baseObj = None
        for obj in context.scene.objects:
            if hasattr(obj, "MhObjectType"):
                if obj.MhObjectType == "Basemesh":
                    baseObj = obj
                    break

        clothesObj = context.active_object

        #
        # set mode to object, especially if you are still in edit mode
        # (otherwise last changes are not used, even assigned groups will not work)
        # since blender could be in multi-editmode we have to do that on both
        # objects, before we do transformation, otherwise transformation is
        # in wrong context
        #
        # apply all transformations on both objects, otherwise it is too hard
        # to determine problems.
        #
        bpy.ops.object.select_all(action='DESELECT')

        if(baseObj.select_get() is False):
            baseObj.select_set(True)

        context.view_layer.objects.active = baseObj
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

        #
        # create filename and check if already existent
        # use alternative path, if one was given
        #
        subdir = context.scene.MHClothesDestination
        if context.scene.MHAltPath != "":
            rootDir = context.scene.MHAltPath
        else:
            rootDir = getClothesRoot(baseObj.MhMeshType, subdir)
        name = clothesObj.MhClothesName
        mc = MakeApparel(context, name, rootDir)

        mhcloexists, dirname =  mc.mhcloExists()

        if context.scene.MHOverwrite is False and mhcloexists:
            bpy.ops.makeapparel.warningbox('INVOKE_DEFAULT', title="Geometry file is already existent, to overwrite change common settings of MakeApparel", info=dirname)
            self.report({'ERROR'}, "no clothes created.")
            return {'FINISHED'}

        #
        # do the checks before shape key is destroyed
        #
        (b, info, error) = checkSanityClothes(clothesObj, baseObj)
        if b:
            bpy.ops.makeapparel.infobox('INVOKE_DEFAULT', title="Check Clothes", info=info, error=error)
            self.report({'ERROR'}, "no clothes created.")
            return {'FINISHED'}

        # all checks done

        #
        # in case that the base has shape keys,
        # add a new one as a mix of all and then remove these one by one
        # so that the last one with its value will be accepted
        #
        if  baseObj.data.shape_keys is not None:
            baseObj.shape_key_add(name=str(baseObj.active_shape_key.name)+"_applied", from_mix=True)
            n = len (baseObj.data.shape_keys.key_blocks)
            baseObj.active_shape_key_index = 0
            for i in range(0, n):
                bpy.ops.object.shape_key_remove(all=False)

        bpy.ops.object.select_all(action='DESELECT')
        if(clothesObj.select_get() is False):
            clothesObj.select_set(True)

        context.view_layer.objects.active = clothesObj
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

        desc = clothesObj.MhClothesDesc
        license = context.scene.MhClothesLicense
        author =  context.scene.MhClothesAuthor

        mc.params(clothesObj, baseObj, license=license, author=author, description=desc, overwriteMaterial=context.scene.MHOverwriteMat)
        (b, hint) = mc.make()
        if b is False:
            self.report({'ERROR'}, hint)
        else:
            self.report({'INFO'}, "Clothes were written to " + dirname)
        return {'FINISHED'}

