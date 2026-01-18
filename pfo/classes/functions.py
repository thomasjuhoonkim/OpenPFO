# logging
from logging import Logger

# classes
from classes.point import Point
from classes.variable import Variable
from classes.objective import Objective

# util
from util.get_config import get_config

config = get_config()

# ==============================================================================


class DefaultParameters:
    def __init__(self, output_case_directory: str, job_id: str, logger: Logger):
        self.output_case_directory = output_case_directory
        self.job_id = job_id
        self.logger = logger


# ==============================================================================


class CreateGeometryParameters:
    """
    NOTE: This does not inherit from DefaultParameters. This is an intentional design choice, we want to avoid modifications to the case directory from this function.
    """

    def __init__(
        self,
        grid_point: Point,
        output_assets_directory: str,
        job_id: str,
        logger: Logger,
    ):
        self.job_id = job_id
        self.grid_point = grid_point
        self.logger = logger
        self.output_assets_directory = output_assets_directory


class CreateGeometryReturn:
    def __init__(
        self,
        output_geometry_filepath: str,
        extra_variables: list[Variable] = [],
    ):
        self.output_geometry_filepath = output_geometry_filepath
        self.extra_variables = extra_variables


# ==============================================================================


class ModifyCaseParameters(DefaultParameters):
    def __init__(
        self,
        output_case_directory: str,
        job_id: str,
        output_geometry_filepath: str,
        logger: Logger,
        grid_point: Point,
        extra_variables: list[Variable],
    ):
        super().__init__(
            output_case_directory=output_case_directory, job_id=job_id, logger=logger
        )
        self.output_geometry_filepath = output_geometry_filepath
        self.grid_point = grid_point
        self.extra_variables = extra_variables
        self.processors = config["compute"]["processors"]


# ==============================================================================


class CreateMeshParameters(DefaultParameters):
    def __init__(
        self,
        output_case_directory: str,
        job_id: str,
        output_geometry_filepath: str,
        logger: Logger,
    ):
        super().__init__(
            output_case_directory=output_case_directory, job_id=job_id, logger=logger
        )
        self.output_geometry_filepath = output_geometry_filepath
        self.processors = config["compute"]["processors"]


# ==============================================================================


class ExecuteSolverParameters(DefaultParameters):
    def __init__(self, output_case_directory: str, job_id: str, logger: Logger):
        super().__init__(
            output_case_directory=output_case_directory, job_id=job_id, logger=logger
        )
        self.processors = config["compute"]["processors"]


# ==============================================================================


class ExtractObjectivesParameters(DefaultParameters):
    def __init__(
        self,
        output_case_directory: str,
        job_id: str,
        logger: Logger,
        objectives: list[Objective],
    ):
        super().__init__(
            output_case_directory=output_case_directory, job_id=job_id, logger=logger
        )
        self.objectives = objectives


class ExtractObjectivesReturn:
    def __init__(self, objectives: list[Objective]):
        self.objectives = objectives


# ==============================================================================


class ExtractAssetsParameters(DefaultParameters):
    def __init__(
        self,
        output_case_directory: str,
        output_case_foam_filepath: str,
        output_assets_directory: str,
        output_geometry_filepath: str,
        job_id: str,
        logger: Logger,
    ):
        super().__init__(
            output_case_directory=output_case_directory, job_id=job_id, logger=logger
        )
        self.output_case_foam_filepath = output_case_foam_filepath
        self.output_assets_directory = output_assets_directory
        self.output_geometry_filepath = output_geometry_filepath
        self.processors = config["compute"]["processors"]


# ==============================================================================


class ExecuteCleanupParameters(DefaultParameters):
    def __init__(self, output_case_directory: str, job_id: str, logger: Logger):
        super().__init__(output_case_directory, job_id, logger)
        self.processors = config["compute"]["processors"]
