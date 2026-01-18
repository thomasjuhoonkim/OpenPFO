# system
import os

# visualization
import pyvista as pv

# datetime
from datetime import datetime

# constants
from constants.job import JobStatus, JobStep
from constants.path import (
    INPUT_CASE_TEMPLATE,
    OUTPUT_ASSETS_DIRECTORY,
    OUTPUT_CASES_DIRECTORY,
)

# classes
from classes.functions import (
    CreateGeometryParameters,
    CreateMeshParameters,
    ExecuteCleanupParameters,
    ExecuteSolverParameters,
    ExtractAssetsParameters,
    ExtractObjectivesParameters,
    ModifyCaseParameters,
)
from classes.point import Point

# PyFOAM
from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory

# util
from util.get_initial_objectives import get_initial_objectives
from util.get_logger import get_logger
from util.get_progress import get_progress

# input
create_geometry = __import__("0_create_geometry")
modify_case = __import__("1_modify_case")
create_mesh = __import__("2_create_mesh")
execute_solver = __import__("3_execute_solver")
extract_objectives = __import__("4_extract_objectives")
extract_assets = __import__("5_extract_assets")
execute_cleanup = __import__("6_execute_cleanup")

logger = get_logger()
progress = get_progress()


class Job:
    def __init__(self, job_id: str, point: Point):
        self._job_id = job_id
        self._point = point

        self._status = JobStatus.INITIALIZED
        self._step = JobStep.INIT
        self._run_ok = True
        self._start_time = None
        self._resolution_time = None
        self._output_geometry_filepath = ""
        self._output_case_directory = f"{OUTPUT_CASES_DIRECTORY}/{job_id}"
        self._output_assets_directory = f"{OUTPUT_ASSETS_DIRECTORY}/{job_id}"
        self._objectives = []
        self._extra_variables = []

        progress.save_job(self)

    def get_id(self):
        return self._job_id

    def get_status(self):
        return self._status.value

    def get_run_ok(self):
        return self._run_ok

    def get_step(self):
        return self._step.value

    def get_start_time(self):
        return self._start_time

    def get_resolution_time(self):
        return self._resolution_time

    def get_case_directory(self):
        return self._output_case_directory

    def get_assets_directory(self):
        return self._output_assets_directory

    def get_point(self):
        return self._point

    def get_objectives(self):
        return self._objectives

    def visualize_geometry(self):
        mesh = pv.read(self._output_geometry_filepath)
        mesh.plot(window_size=[1920, 1080])

    def prepare_job(
        self, should_create_assets_directory=True, should_create_case_directory=True
    ):
        if should_create_assets_directory:
            # create job assets directory
            os.mkdir(self._output_assets_directory)
            logger.info(f"Created assets directory {self._output_assets_directory}")

        if should_create_case_directory:
            # copy case
            base_case = SolutionDirectory(INPUT_CASE_TEMPLATE)
            copy_case = base_case.cloneCase(self._output_case_directory)
            logger.info(f"Generated case directory {copy_case.name}")

        self._status = JobStatus.READY
        self._step = JobStep.PREPARE  # may not need
        progress.save_job(self)

    def dispatch(
        self,
        should_create_geometry=True,
        should_modify_case=True,
        should_create_mesh=True,
        should_execute_solver=True,
        should_extract_objectives=True,
        should_extract_assets=True,
        should_execute_cleanup=True,
    ):
        logger.info(
            f"======================= JOB {self._job_id} START ======================="
        )
        self._start_time = datetime.now()
        self._status = JobStatus.RUNNING
        progress.save_job(self)

        # CREATE GEOMETRY ======================================================
        try:
            if self._run_ok and should_create_geometry:
                logger.info(
                    f"Running create_geometry to generate a geometry for grid point {self._point.get_point_representation()}"
                )
                self._step = JobStep.GEOMETRY
                progress.save_job(self)
                create_geometry_parameters = CreateGeometryParameters(
                    grid_point=self._point,
                    output_assets_directory=self._output_assets_directory,
                    job_id=self._job_id,
                    logger=logger,
                )
                create_geometry_return = create_geometry.create_geometry(
                    create_geometry_parameters=create_geometry_parameters
                )
                self._output_geometry_filepath = (
                    create_geometry_return.output_geometry_filepath
                )
                self._extra_variables = create_geometry_return.extra_variables
            else:
                logger.warning("Skipping create_geometry")
        except Exception:
            self._run_ok = False
            logger.exception("An error occured in create_geometry")
        finally:
            progress.save_job(self)

        # MODIFY CASE ==========================================================
        try:
            if self._run_ok and should_modify_case:
                logger.info("Running modify_case to customize OpenFOAM case")
                self._step = JobStep.CASE
                progress.save_job(self)
                modify_case_parameters = ModifyCaseParameters(
                    output_case_directory=self._output_case_directory,
                    job_id=self._job_id,
                    output_geometry_filepath=self._output_geometry_filepath,
                    logger=logger,
                    grid_point=self._point,
                    extra_variables=self._extra_variables,
                )
                modify_case.modify_case(modify_case_parameters=modify_case_parameters)
            else:
                logger.warning("Skipping modify_case")
        except Exception:
            self._run_ok = False
            logger.exception("An error occured in modify_case")
        finally:
            progress.save_job(self)

        # CREATE MESH ==========================================================
        try:
            if self._run_ok and should_create_mesh:
                logger.info("Running create_mesh to generate a mesh for geometry")
                self._step = JobStep.MESH
                progress.save_job(self)
                create_mesh_parameters = CreateMeshParameters(
                    output_case_directory=self._output_case_directory,
                    job_id=self._job_id,
                    output_geometry_filepath=self._output_geometry_filepath,
                    logger=logger,
                )
                create_mesh.create_mesh(create_mesh_parameters=create_mesh_parameters)
            else:
                logger.warning("Skipping create_mesh")
        except Exception:
            self._run_ok = False
            logger.exception("An error occured in create_mesh")
        finally:
            progress.save_job(self)

        # EXECUTE SOLVER =======================================================
        try:
            if self._run_ok and should_execute_solver:
                logger.info("Running execute_solver to obtain simulation results")
                self._step = JobStep.SOLVE
                progress.save_job(self)
                execute_solver_parameters = ExecuteSolverParameters(
                    output_case_directory=self._output_case_directory,
                    job_id=self._job_id,
                    logger=logger,
                )
                execute_solver.execute_solver(execute_solver_parameters)
            else:
                logger.warning("Skipping execute_solver")
        except Exception:
            self._run_ok = False
            logger.exception("An error occured in execute_solver")
        finally:
            progress.save_job(self)

        # EXTRACT OBJECTIVES ===================================================
        try:
            if self._run_ok and should_extract_objectives:
                logger.info(
                    "Running extract_objectives for objective values extraction"
                )
                self._step = JobStep.OBJECTIVES
                progress.save_job(self)
                extract_objectives_parameters = ExtractObjectivesParameters(
                    output_case_directory=self._output_case_directory,
                    job_id=self._job_id,
                    logger=logger,
                    objectives=get_initial_objectives(),
                )
                extract_objectives_return = extract_objectives.extract_objectives(
                    extract_objectives_parameters=extract_objectives_parameters
                )
                self._objectives = extract_objectives_return.objectives
            else:
                logger.warning("Skipping extract_objectives")
        except Exception:
            self._run_ok = False
            logger.exception("An error occured in extract_objectives")
        finally:
            progress.save_job(self)

        # EXTRACT ASSETS =======================================================
        try:
            if self._run_ok and should_extract_assets:
                logger.info("Running extract_assets for asset extraction")
                self._step = JobStep.ASSETS
                progress.save_job(self)
                extract_assets_parameters = ExtractAssetsParameters(
                    output_case_directory=self._output_case_directory,
                    output_case_foam_filepath=f"{self._output_case_directory}/{self._job_id}.foam",
                    output_assets_directory=self._output_assets_directory,
                    output_geometry_filepath=self._output_geometry_filepath,
                    job_id=self._job_id,
                    logger=logger,
                )
                extract_assets.extract_assets(
                    extract_assets_parameters=extract_assets_parameters
                )
            else:
                logger.warning("Skipping extract_assets")
        except Exception:
            logger.exception("An error occured in extract_assets")
            self._run_ok = False
        finally:
            progress.save_job(self)

        # EXECUTE CLEANUP ======================================================
        try:
            if should_execute_cleanup:  # don't care about run status here
                logger.info("Running execute_cleanup for job cleanup")
                execute_cleanup_parameters = ExecuteCleanupParameters(
                    output_case_directory=self._output_case_directory,
                    job_id=self._job_id,
                    logger=logger,
                )
                execute_cleanup.execute_cleanup(
                    execute_cleanup_parameters=execute_cleanup_parameters
                )
            else:
                logger.warning("Skipping execute_cleanup")
        except Exception:
            self._run_ok = False
            logger.exception("An error occured in execute_cleanup")
        finally:
            progress.save_job(self)

        self._resolution_time = datetime.now()
        if self._run_ok:
            self._status = JobStatus.COMPLETE
        else:
            self._status = JobStatus.FAILED
        progress.save_job(self)

        logger.info(
            f"======================= JOB {self._job_id} END ========================="
        )
