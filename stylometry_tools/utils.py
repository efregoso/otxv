'''
Various classes, utilities, and helpers for stylometry tools.
'''

from enum import Enum
from typing import Required, TypedDict


ERROR_DICT = {
    "CTRL_IS_NONE": ValueError("Control text cannot be None"),
    "SAMP_IS_NONE": ValueError("At least one comparison sample is required"),
    "SAMP_LIST_IS_NONE": ValueError("Comparison samples list cannot be None"),
}


class CharacterFrequencyDict(TypedDict):
    character: Required[str]
    frequency: Required[int]
