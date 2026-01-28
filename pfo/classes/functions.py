# logging
from logging import Logger

# classes
from classes.objective import Objective
from classes.point import Point

# util
from util.get_config import get_config

config = get_config()

# ==============================================================================


class DefaultParameters:
    def __init__(
        self,
        job_id: str,
        point: "Point",
        logger: "Logger",
        job_directory: str,
        processors_per_job=config["compute"]["processors_per_job"],
    ):
        self.processors_per_job = processors_per_job
        self.job_directory = job_directory
        self.job_id = job_id
        self.logger = logger
        self.point = point


class PrepareParameters(DefaultParameters):
    def __init__(
        self,
        job_directory: str,
        logger: "Logger",
        point: "Point",
        job_id: str,
    ):
        super().__init__(
            job_directory=job_directory,
            job_id=job_id,
            logger=logger,
            point=point,
        )


class GeometryParameters(DefaultParameters):
    def __init__(
        self,
        job_directory: str,
        logger: "Logger",
        point: "Point",
        job_id: str,
    ):
        super().__init__(
            job_directory=job_directory,
            job_id=job_id,
            logger=logger,
            point=point,
        )


class MeshParameters(DefaultParameters):
    def __init__(
        self,
        job_directory: str,
        logger: "Logger",
        point: "Point",
        job_id: str,
    ):
        super().__init__(
            job_directory=job_directory,
            logger=logger,
            job_id=job_id,
            point=point,
        )


class SolveParameters(DefaultParameters):
    def __init__(
        self,
        job_directory: str,
        logger: "Logger",
        point: "Point",
        job_id: str,
    ):
        super().__init__(
            job_directory=job_directory,
            logger=logger,
            job_id=job_id,
            point=point,
        )


class ObjectivesParameters(DefaultParameters):
    def __init__(
        self,
        objectives: list["Objective"],
        job_directory: str,
        logger: "Logger",
        point: "Point",
        job_id: str,
    ):
        super().__init__(
            job_directory=job_directory,
            job_id=job_id,
            logger=logger,
            point=point,
        )
        self.objectives = objectives


class CleanupParameters(DefaultParameters):
    def __init__(
        self,
        job_directory: str,
        logger: "Logger",
        point: "Point",
        job_id: str,
    ):
        super().__init__(
            job_directory=job_directory,
            job_id=job_id,
            logger=logger,
            point=point,
        )


# ==============================================================================
class DefaultReturn:
    def __init__(self, run_ok=True):
        self.run_ok = run_ok


class PrepareReturn(DefaultReturn):
    def __init__(self, run_ok=True):
        super().__init__(run_ok=run_ok)


class GeometryReturn(DefaultReturn):
    def __init__(self, visualize_filepath: str, run_ok=True):
        super().__init__(run_ok=run_ok)
        self.visualize_filepath = visualize_filepath


class MeshReturn(DefaultReturn):
    def __init__(self, run_ok=True):
        super().__init__(run_ok=run_ok)


class SolveReturn(DefaultReturn):
    def __init__(self, run_ok=True):
        super().__init__(run_ok=run_ok)


class ObjectivesReturn(DefaultReturn):
    def __init__(self, objectives: list["Objective"], run_ok=True):
        super().__init__(run_ok=run_ok)
        self.objectives = objectives


class CleanupReturn(DefaultReturn):
    def __init__(self, run_ok=True):
        super().__init__(run_ok=run_ok)
