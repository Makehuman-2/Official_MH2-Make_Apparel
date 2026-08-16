#!/usr/bin/python
# -*- coding: utf-8 -*-

import bpy
from ..core_functionality import _loadMeshJson

def EvaluateScalingCallback(self, context):
    _extractScaling = []

    if hasattr (context, "object"):
        baseObj = None
        for obj in context.scene.objects:
            if hasattr(obj, "MhObjectType"):
                if obj.MhObjectType == "Basemesh":
                    baseObj = obj
                    break
        if baseObj is not None:
            (meshtype, jlines) = _loadMeshJson(baseObj)
            cnt = 1
            _extractScaling.append(("identity", "Identity", "No different Scale", cnt))
            cnt += 1
            for gname in jlines["dimensions"]:
                gl_name = gname.lower()
                _extractScaling.append((gname, gl_name.capitalize(), "Use scaling of " + gl_name, cnt))
                cnt += 1
    return (_extractScaling)

def EvaluateRigidCallback(self, context):
    _rigids = []

    if hasattr (context, "object"):
        baseObj = None
        for obj in context.scene.objects:
            if hasattr(obj, "MhObjectType"):
                if obj.MhObjectType == "Basemesh":
                    baseObj = obj
                    break
        if baseObj is not None:
            (meshtype, jlines) = _loadMeshJson(baseObj)
            cnt = 1
            _rigids.append(("not rigid", "Not rigid", "Not rigid", cnt))
            cnt += 1
            for gname in jlines["rigid"]:
                gl_name = gname.lower()
                _rigids.append((gname, gl_name.capitalize(), "Connect to " + gl_name, cnt))
                cnt += 1
    return (_rigids)

class MHC_OT_GetOffsetScaling(bpy.types.Operator):
    """Select an offset scaling used to get the dimensions for clothes. Identity is scale factor 1.0."""
    bl_idname = "makeapparel.offset_scaling"
    bl_label = "Offset Scaling"
    bl_options = {'REGISTER', 'UNDO'}

    scaling: bpy.props.EnumProperty(items=EvaluateScalingCallback, name="scaling", description="Offset-Scaling")

    @classmethod
    def poll(self, context):
        if context.active_object is not None:
            if not hasattr(context.active_object, "MhObjectType"):
                return False
            if context.active_object.select_get():
                if context.active_object.MhObjectType != "Basemesh":
                    return True
        return False

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=300)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'scaling')

    def execute(self, context):
        context.active_object.MhOffsetScale =  self.scaling
        self.report({'INFO'}, "Scaling is based on " + self.scaling)
        context.area.tag_redraw()
        return {'FINISHED'}

class MHC_OT_GetRigid(bpy.types.Operator):
    """Select a rigid vertex group for clothes. If it is not rigid or you use own vertex groups, the value must be None."""
    bl_idname = "makeapparel.get_rigid"
    bl_label = "Rigid Group"
    bl_options = {'REGISTER', 'UNDO'}

    rigid: bpy.props.EnumProperty(items=EvaluateRigidCallback, name="rigid", description="Rigid group")

    @classmethod
    def poll(self, context):
        if context.active_object is not None:
            if not hasattr(context.active_object, "MhObjectType"):
                return False
            if context.active_object.select_get():
                if context.active_object.MhObjectType != "Basemesh":
                    return True
        return False

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=300)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'rigid')

    def execute(self, context):
        context.active_object.MhRigid =  self.rigid
        self.report({'INFO'}, "Rigid will use " + self.rigid)
        context.area.tag_redraw()
        return {'FINISHED'}
