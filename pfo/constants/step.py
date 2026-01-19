from enum import Enum


class StepId(Enum):
    CREATE_GEOMETRY = "create_geometry"
    MODIFY_CASE = "modify_case"
    CREATE_MESH = "create_mesh"
    EXECUTE_SOLVER = "execute_solver"
    EXTRACT_OBJECTIVES = "extract_objectives"
    EXTRACT_ASSETS = "extract_assets"
    EXECUTE_CLEANUP = "execute_cleanup"
