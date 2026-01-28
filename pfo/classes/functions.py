# logging
from logging import Logger

# classes
from classes.objective import Objective
from classes.point import Point

# util
from constants.path import OUTPUT_ASSETS_DIRECTORY
from util.get_config import get_config

config = get_config()

# ==============================================================================


class DefaultParameters:
    def __init__(
        self,
        job_id: str,
        point: "Point",
        logger: "Logger",
        output_assets_directory=OUTPUT_ASSETS_DIRECTORY,
        processors_per_job=config["compute"]["processors_per_job"],
    ):
        self.output_assets_directory = output_assets_directory
        self.processors_per_job = processors_per_job
        self.job_id = job_id
        self.logger = logger
        self.point = point


class DefaultReturn:
    def __init__(self, run_ok=True):
        self.run_ok = run_ok


# ==============================================================================


class CreateGeometryParameters(DefaultParameters):
    def __init__(
        self,
        logger: "Logger",
        point: "Point",
        job_id: str,
    ):
        super().__init__(
            job_id=job_id,
            logger=logger,
            point=point,
        )


class CreateGeometryReturn(DefaultReturn):
    def __init__(self, run_ok=True):
        super().__init__(run_ok=run_ok)


# ==============================================================================


class ModifyCaseParameters(DefaultParameters):
    def __init__(
        self,
        logger: "Logger",
        point: "Point",
        job_id: str,
    ):
        super().__init__(
            job_id=job_id,
            logger=logger,
            point=point,
        )


class ModifyCaseReturn(DefaultReturn):
    def __init__(self, run_ok=True):
        super().__init__(run_ok=run_ok)


# ==============================================================================


class CreateMeshParameters(DefaultParameters):
    def __init__(
        self,
        logger: "Logger",
        point: "Point",
        job_id: str,
    ):
        super().__init__(
            logger=logger,
            job_id=job_id,
            point=point,
        )


class CreateMeshReturn(DefaultReturn):
    def __init__(self, run_ok=True):
        super().__init__(run_ok=run_ok)


# ==============================================================================


class ExecuteSolverParameters(DefaultParameters):
    def __init__(
        self,
        logger: "Logger",
        point: "Point",
        job_id: str,
    ):
        super().__init__(
            logger=logger,
            job_id=job_id,
            point=point,
        )


class ExecuteSolverReturn(DefaultReturn):
    def __init__(self, run_ok=True):
        super().__init__(run_ok=run_ok)


# ==============================================================================


class ExtractObjectivesParameters(DefaultParameters):
    def __init__(
        self,
        objectives: list["Objective"],
        logger: "Logger",
        point: "Point",
        job_id: str,
    ):
        super().__init__(
            job_id=job_id,
            logger=logger,
            point=point,
        )
        self.objectives = objectives


class ExtractObjectivesReturn(DefaultReturn):
    def __init__(self, objectives: list["Objective"], run_ok=True):
        super().__init__(run_ok=run_ok)
        self.objectives = objectives


# ==============================================================================


class ExtractAssetsParameters(DefaultParameters):
    def __init__(
        self,
        logger: "Logger",
        point: "Point",
        job_id: str,
    ):
        super().__init__(
            job_id=job_id,
            logger=logger,
            point=point,
        )


class ExtractAssetsReturn(DefaultReturn):
    def __init__(self, run_ok=True):
        super().__init__(run_ok=run_ok)


# ==============================================================================


class ExecuteCleanupParameters(DefaultParameters):
    def __init__(
        self,
        job_id: str,
        logger: "Logger",
        point: "Point",
    ):
        super().__init__(
            job_id=job_id,
            logger=logger,
            point=point,
        )


class ExecuteCleanupReturn(DefaultReturn):
    def __init__(self, run_ok=True):
        super().__init__(run_ok=run_ok)
