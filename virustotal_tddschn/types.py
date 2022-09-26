#!/usr/bin/env python3

from pathlib import Path
from typing import Literal, TypedDict

class BrewType(TypedDict):
    f: Literal[0, 1]
    c: Literal[0, 1]

BrewPaths = list[Path]

class BrewTypeAndPaths(TypedDict):
    brew_type: BrewType
    formula_paths: BrewPaths
    cask_paths: BrewPaths