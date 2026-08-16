#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Author: black-punkduck, Elvaerwyn

from .extractclothes import MHC_OT_ExtractClothesOperator
from .importmhclo import MHC_OT_ImportClothesOperator
from .markasclothes import MHC_OT_MarkAsClothesOperator
from .markasbase import MHC_OT_MarkAsBaseOperator
from .importbase import MHC_OT_ImportBaseOperator
from .checkclothes import MHC_OT_CheckClothesOperator
from .createclothes import MHC_OT_CreateClothesOperator
from .checkbase import MHC_OT_CheckBaseOperator
from .apply_shapekeys import MHC_OT_ApplyShapeKeysOperator
from .deletehelper import MHC_OT_DeleteHelper
from .tagselector import MHC_OT_TagSelector
from .importpredef import MHC_OT_Predefined
from .offsetscaling import MHC_OT_GetOffsetScaling, MHC_OT_GetRigid

OPERATOR_CLASSES = [
    MHC_OT_ExtractClothesOperator,
    MHC_OT_ImportClothesOperator,
    MHC_OT_MarkAsClothesOperator,
    MHC_OT_MarkAsBaseOperator,
    MHC_OT_ImportBaseOperator,
    MHC_OT_CheckClothesOperator,
    MHC_OT_CreateClothesOperator,
    MHC_OT_CheckBaseOperator,
    MHC_OT_ApplyShapeKeysOperator,
    MHC_OT_DeleteHelper,
    MHC_OT_TagSelector,
    MHC_OT_Predefined,
    MHC_OT_GetOffsetScaling,
    MHC_OT_GetRigid
]

__all__ = [
    "MHC_OT_ExtractClothesOperator",
    "MHC_OT_ImportClothesOperator",
    "MHC_OT_MarkAsClothesOperator",
    "MHC_OT_MarkAsBaseOperator",
    "MHC_OT_ImportBaseOperator",
    "MHC_OT_CheckClothesOperator",
    "MHC_OT_CreateClothesOperator",
    "MHC_OT_CheckBaseOperator",
    "MHC_OT_ApplyShapeKeysOperator",
    "MHC_OT_DeleteHelper",
    "MHC_OT_TagSelector",
    "MHC_OT_Predefined",
    "MHC_OT_GetOffsetScaling",
    "MHC_OT_GetRigid",
    "OPERATOR_CLASSES"
]
