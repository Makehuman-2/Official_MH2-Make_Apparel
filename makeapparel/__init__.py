#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Authors: black-punkduck (Maintainer)
#            Elvaerwyn
#
# must be before(!) all imports
#
bl_info = {
    "name": "MakeApparel",
    "author": "black-punkduck, Elvaerwyn",
    "version": (3,0,0),
    "blender": (4,0,0),
    "location": "View3D > Properties > MakeApparel",
    "description": "Create MakeHuman2 Fashion and Assets",
    'wiki_url': "https://makehuman-2.github.io/",
    "category": "MakeHuman2"}

from bpy.utils import register_class, unregister_class
import bpy
from .extraproperties import extraProperties
from .makeapparel import MHC_PT_MakeApparelPanel
from .material import MHC_OT_ImportMaterialOperator, MHC_OT_CreateMaterialOperator, MHC_OT_WriteMaterialOperator
from .infobox import MHC_OT_InfoBox,MHC_OT_WarningBox
from .operators import *
MAKEAPPAREL_CLASSES = []
MAKEAPPAREL_CLASSES.extend(OPERATOR_CLASSES)
MAKEAPPAREL_CLASSES.append(MHC_PT_MakeApparelPanel)
MAKEAPPAREL_CLASSES.append(MHC_OT_ImportMaterialOperator)
MAKEAPPAREL_CLASSES.append(MHC_OT_CreateMaterialOperator)
MAKEAPPAREL_CLASSES.append(MHC_OT_WriteMaterialOperator)
MAKEAPPAREL_CLASSES.append(MHC_OT_InfoBox)
MAKEAPPAREL_CLASSES.append(MHC_OT_WarningBox)

__all__ = [
    "MHC_PT_MakeApparelPanel",
    "MHC_OT_InfoBox",
    "MHC_OT_WarningBox",
    "MHC_OT_ImportMaterialOperator",
    "MHC_OT_CreateMaterialOperator",
    "MAKEAPPAREL_CLASSES"
]

def register():
    extraProperties()
    for cls in MAKEAPPAREL_CLASSES:
        register_class(cls)

    bpy.types.Scene.mcTabs = bpy.props.EnumProperty(
    name='MeshOrMaterial',
    items = (
             ('A'  , "Mesh"  , "Operators related meshes"),
             ('B', "Material", "Material editor")
        ),
    default = 'A'
    )


def unregister():

    for cls in reversed(MAKEAPPAREL_CLASSES):
        unregister_class(cls)

if __name__ == "__main__":
    register()
    print("MaleApparel loaded")

