from enum import Enum


class StepId(Enum):
    PREPARE = "prepare"
    GEOMETRY = "geometry"
    MESH = "mesh"
    SOLVE = "solve"
    OBJECTIVES = "objectives"
    CLEANUP = "cleanup"
