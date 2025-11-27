from logging import Logger
from classes.point import Point

# ==============================================================================


class DefaultParameters:
    def __init__(self, output_case_directory: str, job_id: str, logger: Logger):
        self.output_case_directory = output_case_directory
        self.job_id = job_id
        self.logger = logger


class DefaultReturn:
    def __init__(self, run_ok: bool):
        self.run_ok = run_ok


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


class CreateGeometryReturn(DefaultReturn):
    def __init__(self, run_ok: bool, output_geometry_filepath: str):
        super().__init__(run_ok=run_ok)
        self.output_geometry_filepath = output_geometry_filepath


# ==============================================================================


class ModifyCaseParameters(DefaultParameters):
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


class ModifyCaseReturn(DefaultReturn):
    def __init__(self, run_ok):
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
    def __init__(self, run_ok):
        super().__init__(run_ok=run_ok)


# ==============================================================================


class ExecuteSolverParameters(DefaultParameters):
    def __init__(self, output_case_directory: str, job_id: str, logger: Logger):
        super().__init__(
            output_case_directory=output_case_directory, job_id=job_id, logger=logger
        )


class ExecuteSolverReturn(DefaultReturn):
    def __init__(self, run_ok):
        super().__init__(run_ok=run_ok)


# ==============================================================================


class ExtractObjectivesParameters(DefaultParameters):
    def __init__(self, output_case_directory: str, job_id: str, logger: Logger):
        super().__init__(
            output_case_directory=output_case_directory, job_id=job_id, logger=logger
        )


class ExtractObjectivesReturn(DefaultReturn):
    def __init__(self, run_ok: bool, objectives: list[float]):
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
    def __init__(self, run_ok):
        super().__init__(run_ok=run_ok)


# ==============================================================================


class ExecuteCleanupParameters(DefaultParameters):
    def __init__(self, output_case_directory: str, job_id: str, logger: Logger):
        super().__init__(output_case_directory, job_id, logger)


class ExecuteCleanupReturn(DefaultReturn):
    def __init__(self, run_ok):
        super().__init__(run_ok=run_ok)
