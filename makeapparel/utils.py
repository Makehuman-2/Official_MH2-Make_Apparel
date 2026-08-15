#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Author: black-punkduck, Elvaerwyn

import os
import json
import io
import sys
import bpy
import inspect
from addon_utils import check, paths, enable, modules

# we need this for the standard obj-loader 
#
from mathutils import Matrix
from bpy_extras.io_utils import axis_conversion

if bpy.app.version < (4,0,0):
    from io_scene_obj import import_obj

def getMyDocuments():
    import sys
    if sys.platform == 'win32':
        import winreg
        try:
            k = winreg.HKEY_CURRENT_USER
            for x in ['Software', 'Microsoft', 'Windows', 'CurrentVersion', 'Explorer', 'Shell Folders']:
                k = winreg.OpenKey(k, x)

            name, type = winreg.QueryValueEx(k, 'Personal')

            if type == 1:
                return name
        except Exception as e:
            print("Did not find path to My Documents folder")
    elif sys.platform.startswith('linux'):

        # Default path to xdg configuration file
        CONFIG_PATH = os.path.expanduser('~/.config/user-dirs.dirs')
        doc_folder = None
        if os.path.isfile(CONFIG_PATH):
            with io.open(CONFIG_PATH , 'r') as file:
                for line in file:
                    if line and line.startswith('XDG_DOCUMENTS_DIR'):
                        line = line.strip()
                        key, value = line.split('=')
                        value = os.path.expandvars(value.strip('"'))
                        if os.path.isdir(value):
                            doc_folder = value
        if doc_folder is None:
            doc_folder = os.path.expanduser("~")



def pathFromConfigFile():
    configFile = ''
    if sys.platform.startswith('linux'):
        configFile = os.path.expanduser('~/.config/makehuman2/makehuman2.conf')

    elif sys.platform.startswith('darwin'):
        configFile = os.path.expanduser('~/Library/Application Support/MakeHuman2/makehuman2.conf')

    elif sys.platform.startswith('win32'):
        configFile = os.path.join(os.getenv('LOCALAPPDATA', ''), 'makehuman2', 'makehuman2.conf')
        if not os.path.isfile(configFile):
            # check for virtual environment (hopefully only one python interpreter given)
            packagedir = os.path.join(os.getenv('LOCALAPPDATA', ''), 'Packages')
            pythonInterpreter = []
            for f in os.listdir(packagedir):
                if f.startswith("PythonSoftwareFoundation.Python.") and os.path.isdir(os.path.join(packagedir, f)):
                    pythonInterpreter.append(f)
            if len(pythonInterpreter) == 1:
                configFile = os.path.join(packagedir, pythonInterpreter[0], "LocalCache", "Local", "makehuman2", "makehuman2.conf") 
    configPath = ''

    if os.path.isfile(configFile):
        with open(configFile) as f:
            jdict = json.load(f)
        if "path_home" in jdict:
            configPath = jdict["path_home"]

    homepath = ""
    if os.path.isdir(configPath):
        homepath = os.path.normpath(configPath).replace("\\", "/")
    return (homepath)


def getClothesRoot(mesh, subdir=None):
    if subdir is None:
        subdir = "clothes"
    mhdir = pathFromConfigFile()

    if len(mhdir) == 0:
        mhdir = getMyDocuments()

    if mesh is None:
        return os.path.join(mhdir,"data",subdir)
    else:
        return os.path.join(mhdir,"data",subdir,mesh)

def getMHUserRoot():
    mydocs = pathFromConfigFile()

    if len(mydocs) == 0:
        mydocs = getMyDocuments()

    return os.path.join(mydocs, "data")

# 
# function to call standard object loader
#
def loadObjFile(context, filename):
    #
    # remember all objects
    #
    oldnames = []
    for obj in context.scene.objects:
        oldnames.append (obj.name)

    if bpy.app.version >= (4,0,0):
        bpy.ops.wm.obj_import(filepath=filename, use_split_objects=False, import_vertex_groups=True)
    else:
        global_matrix = (Matrix.Scale(1.0, 4) @
            axis_conversion(from_forward='-Y',to_forward='-Z', from_up='Z', to_up='-Y',).to_4x4())
        import_obj.load(context, filename, use_split_objects=False,
            use_groups_as_vgroups=True, global_matrix=global_matrix)

    #
    # get all objects and figure out the new mesh
    #
    for obj in context.scene.objects:
        if obj.name not in oldnames:
           context.view_layer.objects.active = obj
           bpy.ops.object.shade_smooth()
           bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
           return (obj)

    return (None)

