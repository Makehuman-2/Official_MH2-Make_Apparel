#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Author: black-punkduck

# layout:
#
# [preferences/common-settings]
# [get & check base]
# [get & check clothes]
# [create clothes]

import bpy
from . import bl_info   # to get information about version
from .utils import getMHUserRoot

class MHC_PT_MakeApparelPanel(bpy.types.Panel):
    bl_label = bl_info["name"] + " v %d.%d.%d" % bl_info["version"]
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MakeApparel"

    def draw(self, context):
        layout = self.layout
        scn = context.scene

        base_available = False
        shape_keys = False
        for obj in scn.objects:
            if hasattr(obj, "MhObjectType"):
                if obj.MhObjectType == "Basemesh":
                    base_available = True
                    if  obj.data.shape_keys is not None:
                        shape_keys = True
                    break

        obj = context.active_object

        # common settings (always displayed)
        #
        commonSettingsBox = layout.box()
        commonSettingsBox.label(text="Common settings", icon="TOOL_SETTINGS")
        col = commonSettingsBox.column()
        row = col.row()
        row.prop(scn, 'MHOverwrite', text="Overwrite existent geometry")
        row = col.row()
        row.prop(scn, 'MHOverwriteMat', text="Overwrite existent material")
        row = col.row()
        row.prop(scn, 'MhMsOverwrite', text="Replace materials for blender objects")
        row = col.row()
        row.prop(scn, 'MHAllowMods', text="Allow modifiers")
        row = col.row()
        row.label(text="License")
        row.prop(scn, 'MhClothesLicense', text="")
        row = col.row()
        row.label(text="Author")
        row.prop(scn, 'MhClothesAuthor', text="")

        layout.prop(scn, 'mcTabs', expand=True)

        if scn.mcTabs == 'A':
            # get and check base
            #
            baseBox = layout.box()
            baseBox.label(text="Base", icon="MESH_DATA")
            if hasattr(obj, "MhMeshType"):
                row = baseBox.row()
                row.label(text="Basename")
                row.prop(obj, 'MhMeshType', text="")
                meshtype = obj.MhMeshType
            else:
                meshtype = None

            if not base_available:
                if scn.MH_predefinedMeshes != "---":
                    baseBox.prop(scn, 'MH_predefinedMeshes')
                    baseBox.operator("makeapparel.importpredef", text="Import predefined base")
                baseBox.operator("makeapparel.importbase", text="Import base (.obj)")

            baseBox.operator("makeapparel.mark_as_base", text="Mark as base")
            baseBox.operator("makeapparel.check_base", text="Check base")
            if meshtype == "hm08":
                baseBox.operator("makeapparel.delete_helper", text="Delete helpers")
            if  shape_keys:
                baseBox.operator("makeapparel.apply_shapekeys", text="Apply targets")

            # get and check clothes (same order as base)
            #
            setupBox = layout.box()
            setupBox.label(text="Clothes", icon="MESH_DATA")

            if meshtype == "hm08":
                setupBox.label(text="Optional base for clothes:")
                setupBox.operator("makeapparel.extract_clothes", text="Extract from Helper")

            setupBox.label(text="Edit existent clothes:")
            setupBox.operator("makeapparel.import_mhclo", text="Import clothes file")

            setupBox.operator("makeapparel.mark_as_clothes", text="Mark as clothes")

            setupBox.operator("makeapparel.check_clothes", text="Check clothes")

            # the procedure itself
            #
            produceBox = layout.box()
            produceBox.label(text="Produce clothes", icon="MOD_CLOTH")
            if obj is None or obj.type != "MESH":
                produceBox.label(text="- select a visible mesh object -")
            else:
                if obj.MhObjectType == "Basemesh":
                    produceBox.label(text="Selected mesh is marked as base")
                else:
                    produceBox.label(text="Name")
                    produceBox.prop(obj, 'MhClothesName', text="")
                    produceBox.label(text="Description")
                    produceBox.prop(obj, 'MhClothesDesc', text="")
                    produceBox.operator("makeapparel.tag_selector", text="Edit tags")
                    col = produceBox.column()
                    row = col.row()
                    row.label(text="Z-Depth")
                    row.prop(obj, 'MhZDepth', text="")
                    produceBox.operator("makeapparel.offset_scaling", text="Change Scaling: "+ obj.MhOffsetScale)
                    produceBox.operator("makeapparel.get_rigid", text="Change Rigid: "+ obj.MhRigid)
                    produceBox.label(text="Delete-Group on Base-Mesh")
                    produceBox.prop(obj, 'MhDeleteGroup', text="")
                    datafolder = getMHUserRoot()
                    produceBox.label(text="Data folder MakeHuman II")
                    produceBox.label(text=datafolder)
                    row = produceBox.row()
                    row.label(text="Alternative path:")
                    row.prop(scn, 'MHAltPath', text="")
                    produceBox.label(text="Destination subdir")
                    produceBox.prop(scn, 'MHClothesDestination', text="")
                    produceBox.operator("makeapparel.create_clothes", text="Make clothes")
        else:
            createBox = layout.box()
            if obj is None or obj.type != "MESH":
                createBox.label(text="- select a visible mesh object -")
            else:
                createBox.label(text="Create material", icon="MESH_DATA")
                createBox.prop(scn, 'MhMsCreateDiffuse', text="Diffuse texture")
                createBox.prop(scn, 'MhMsCreateNormal', text="Normal map")
                createBox.prop(scn, 'MhMsCreateRoughMetal', text="Roughness-Metal map")
                createBox.prop(scn, 'MhMsCreateAOMap', text="Ambient occlusion map")
                createBox.prop(scn, 'MhMsCreateEmission', text="Emission map")
                createBox.operator("makeapparel.create_material", text="Create material")

            importBox = layout.box()
            importBox.label(text="Import material", icon="MESH_DATA")
            importBox.operator("makeapparel.import_material", text="Import material")

            writeBox = layout.box()
            writeBox.label(text="Write material", icon="MATERIAL_DATA")

            if obj is not None:
                writeBox.prop(obj, 'MhMsName', text='Name')
                writeBox.prop(obj, 'MhMsDescription', text='Description')
                writeBox.prop(obj, 'MhMsTag', text='Tags')
                writeBox.prop(obj, 'MhMsShader', text='Shader')

                writeBox.prop(obj, 'MhMsBackfaceCull', text='Backface culling')
                writeBox.prop(obj, 'MhMsAlphaToCoverage', text='AlphaToCoverage')
                writeBox.prop(obj, 'MhMsTransparent', text='Transparent')
                writeBox.prop(obj, 'MhMsTextures', text='Paths')
                writeBox.prop(obj, 'MhMsUseLit', text='Use litsphere')
                writeBox.prop(obj, 'MhMsLitsphere', text='Litsphere texture')

                writeBox.operator("makeapparel.write_material", text="Save material")
