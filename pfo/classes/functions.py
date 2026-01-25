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
        self.processors_per_job = config["compute"]["processors_per_job"]


class DefaultReturn:
    def __init__(self, run_ok=True):
        self.run_ok = run_ok


# ==============================================================================


class CreateGeometryParameters:
    """
    NOTE: This does not inherit from DefaultParameters. This is an intentional design choice, we want to avoid modifications to the case directory from this function.
    """

    def __init__(
        self,
        point: Point,
        output_assets_directory: str,
        job_id: str,
        logger: Logger,
    ):
        self.job_id = job_id
        self.point = point
        self.logger = logger
        self.output_assets_directory = output_assets_directory
        self.processors_per_job = config["compute"]["processors_per_job"]


class CreateGeometryReturn(DefaultReturn):
    def __init__(
        self,
        output_geometry_filepath: str,
        run_ok=True,
        extra_variables: list[Variable] | None = None,
    ):
        super().__init__(run_ok=run_ok)
        self.output_geometry_filepath = output_geometry_filepath
        self.extra_variables = extra_variables if extra_variables is not None else []


# ==============================================================================


class ModifyCaseParameters(DefaultParameters):
    def __init__(
        self,
        output_case_directory: str,
        job_id: str,
        output_geometry_filepath: str,
        logger: Logger,
        point: Point,
        extra_variables: list[Variable],
    ):
        super().__init__(
            output_case_directory=output_case_directory, job_id=job_id, logger=logger
        )
        self.output_geometry_filepath = output_geometry_filepath
        self.point = point
        self.extra_variables = extra_variables


class ModifyCaseReturn(DefaultReturn):
    def __init__(self, run_ok=True):
        super().__init__(run_ok=run_ok)


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


class CreateMeshReturn(DefaultReturn):
    def __init__(self, run_ok=True):
        super().__init__(run_ok=run_ok)


# ==============================================================================


class ExecuteSolverParameters(DefaultParameters):
    def __init__(self, output_case_directory: str, job_id: str, logger: Logger):
        super().__init__(
            output_case_directory=output_case_directory, job_id=job_id, logger=logger
        )


class ExecuteSolverReturn(DefaultReturn):
    def __init__(self, run_ok=True):
        super().__init__(run_ok=run_ok)


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


class ExtractObjectivesReturn(DefaultReturn):
    def __init__(self, objectives: list[Objective], run_ok=True):
        super().__init__(run_ok=run_ok)
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


class ExtractAssetsReturn(DefaultReturn):
    def __init__(self, run_ok=True):
        super().__init__(run_ok)


# ==============================================================================


class ExecuteCleanupParameters(DefaultParameters):
    def __init__(self, output_case_directory: str, job_id: str, logger: Logger):
        super().__init__(output_case_directory, job_id, logger)


class ExecuteCleanupReturn(DefaultReturn):
    def __init__(self, run_ok=True):
        super().__init__(run_ok=run_ok)
