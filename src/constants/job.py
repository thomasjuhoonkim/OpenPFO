from enum import Enum


class JobStatus(Enum):
    INITIALIZED = "initialized"
    READY = "ready"
    RUNNING = "running"
    FAILED = "failed"
    COMPLETE = "complete"


class JobStep(Enum):
    INIT = "init"
    PREPARE = "prepare"
    GEOMETRY = "geometry"
    CASE = "case"
    MESH = "mesh"
    SOLVE = "solve"
    OBJECTIVES = "objectives"
    ASSETS = "assets"
