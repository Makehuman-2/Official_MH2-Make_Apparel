#!/usr/bin/python
# -*- coding: utf-8 -*-

import bpy
from ..sanitychecks import checkSanityBase

class MHC_OT_CheckBaseOperator(bpy.types.Operator):
    """Check base object if it is usable for makeapparel"""
    bl_idname = "makeapparel.check_base"
    bl_label = "Check base"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(self, context):
        if context.active_object is not None:
            if not hasattr(context.active_object, "MhObjectType"):
                return False
            if context.active_object.select_get():
                if context.active_object.MhObjectType == "Basemesh":
                    return True
        return False

    def execute(self, context):
        # set mode to object, especially if you are still in edit mode
        # (otherwise last changes are not used
        bpy.ops.object.mode_set(mode='OBJECT')

        (b, info, error) = checkSanityBase(context)
        bpy.ops.makeapparel.infobox('INVOKE_DEFAULT', title="Check Base", info=info, error=error)
        return {'FINISHED'}
