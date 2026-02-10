# logging
from logging import Logger

# classes
from classes.objective import Objective
from classes.point import Point
from classes.meta import Meta

# util
from util.get_config import get_config

config = get_config()

# ==============================================================================


class DefaultParameters:
    def __init__(
        self,
        job_id: str,
        meta: "Meta",
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
        self.meta = meta


class PrepareParameters(DefaultParameters):
    def __init__(
        self,
        job_directory: str,
        logger: "Logger",
        point: "Point",
        meta: "Meta",
        job_id: str,
    ):
        super().__init__(
            job_directory=job_directory,
            job_id=job_id,
            logger=logger,
            point=point,
            meta=meta,
        )


class GeometryParameters(DefaultParameters):
    def __init__(
        self,
        job_directory: str,
        logger: "Logger",
        point: "Point",
        meta: "Meta",
        job_id: str,
    ):
        super().__init__(
            job_directory=job_directory,
            job_id=job_id,
            logger=logger,
            point=point,
            meta=meta,
        )


class MeshParameters(DefaultParameters):
    def __init__(
        self,
        job_directory: str,
        logger: "Logger",
        point: "Point",
        meta: "Meta",
        job_id: str,
    ):
        super().__init__(
            job_directory=job_directory,
            logger=logger,
            job_id=job_id,
            point=point,
            meta=meta,
        )


class SolveParameters(DefaultParameters):
    def __init__(
        self,
        job_directory: str,
        logger: "Logger",
        point: "Point",
        meta: "Meta",
        job_id: str,
    ):
        super().__init__(
            job_directory=job_directory,
            logger=logger,
            job_id=job_id,
            point=point,
            meta=meta,
        )


class ObjectivesParameters(DefaultParameters):
    def __init__(
        self,
        objectives: list["Objective"],
        job_directory: str,
        logger: "Logger",
        point: "Point",
        meta: "Meta",
        job_id: str,
    ):
        super().__init__(
            job_directory=job_directory,
            job_id=job_id,
            logger=logger,
            point=point,
            meta=meta,
        )
        self.objectives = objectives


class CleanupParameters(DefaultParameters):
    def __init__(
        self,
        job_directory: str,
        logger: "Logger",
        point: "Point",
        meta: "Meta",
        job_id: str,
    ):
        super().__init__(
            job_directory=job_directory,
            job_id=job_id,
            logger=logger,
            point=point,
            meta=meta,
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
