# system
import os

# datetime
from datetime import datetime

# typing
from typing import TYPE_CHECKING

# constants
from constants.job import JobStatus
from constants.step import StepId
from constants.path import (
    INPUT_CASE_TEMPLATE,
    OUTPUT_ASSETS_DIRECTORY,
    OUTPUT_CASES_DIRECTORY,
)

# numpy
import numpy as np

# classes
if TYPE_CHECKING:
    from classes.progress import Progress
from classes.functions import (
    CreateGeometryParameters,
    CreateMeshParameters,
    ExecuteCleanupParameters,
    ExecuteSolverParameters,
    ExtractAssetsParameters,
    ExtractObjectivesParameters,
    ModifyCaseParameters,
)
from classes.objective import Objective
from classes.variable import Variable
from classes.point import Point
from classes.step import Step

# PyFoam
from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile

# util
from util.get_config_objectives import get_config_objectives
from util.get_config import get_config
from util.get_logger import get_logger

# input
create_geometry = __import__("0_create_geometry")
modify_case = __import__("1_modify_case")
create_mesh = __import__("2_create_mesh")
execute_solver = __import__("3_execute_solver")
extract_objectives = __import__("4_extract_objectives")
extract_assets = __import__("5_extract_assets")
execute_cleanup = __import__("6_execute_cleanup")

config = get_config()
logger = get_logger()

# visualization
IS_HPC = config["compute"]["hpc"]
if not IS_HPC:
    import pyvista as pv


class Job:
    def __init__(
        self,
        id: str,
        point: "Point",
        progress: "Progress",
        # defaults
        steps: list["Step"] | None = None,
        status: JobStatus | None = None,
        run_ok=True,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        output_geometry_filepath="",
        output_case_directory="",
        output_assets_directory="",
        objectives: list["Objective"] | None = None,
        extra_variables: list["Variable"] | None = None,
    ):
        self._id = id
        self._point = point
        self._progress = progress
        self._steps = steps if steps is not None else []
        self._status = status if status is not None else JobStatus.INITIALIZED
        self._run_ok = run_ok
        self._start_time = start_time if start_time is not None else datetime.now()
        self._end_time = end_time if end_time is not None else datetime.now()
        self._output_geometry_filepath = output_geometry_filepath
        self._output_case_directory = (
            output_case_directory
            if output_case_directory
            else f"{OUTPUT_CASES_DIRECTORY}/{id}"
        )
        self._output_assets_directory = (
            output_assets_directory
            if output_assets_directory
            else f"{OUTPUT_ASSETS_DIRECTORY}/{id}"
        )
        self._objectives = objectives if objectives is not None else []
        self._extra_variables = extra_variables if extra_variables is not None else []

        self._progress.save_job(self)

    def get_id(self):
        return self._id

    def get_status(self):
        return self._status

    def get_run_ok(self):
        return self._run_ok

    def get_steps(self):
        return self._steps

    def get_start_time(self):
        return self._start_time

    def get_end_time(self):
        return self._end_time

    def get_output_geometry_filepath(self):
        return self._output_geometry_filepath

    def get_output_case_directory(self):
        return self._output_case_directory

    def get_output_assets_directory(self):
        return self._output_assets_directory

    def get_point(self):
        return self._point

    def get_objectives(self):
        return self._objectives

    def visualize_geometry(self):
        if not IS_HPC:
            mesh = pv.read(self._output_geometry_filepath)
            mesh.plot(window_size=[1920, 1080])
        else:
            logger.warning(
                "config.compute.hpc is set true, geometry visualization with PyVista is unavailable."
            )

    def prepare_job(
        self, should_create_assets_directory=True, should_create_case_directory=True
    ):
        if should_create_assets_directory:
            # create job assets directory
            os.makedirs(self._output_assets_directory)
            logger.info(f"Created assets directory {self._output_assets_directory}")

        if should_create_case_directory:
            # copy case
            os.makedirs(self._output_case_directory)
            base_case = SolutionDirectory(INPUT_CASE_TEMPLATE)
            copy_case = base_case.cloneCase(self._output_case_directory)
            logger.info(f"Generated case directory {copy_case.name}")

            # decomposeParDict subdomains
            decompose_par_dict_filepath = (
                f"{self._output_case_directory}/system/decomposeParDict"
            )
            decompose_par_dict = ParsedParameterFile(decompose_par_dict_filepath)
            decompose_par_dict["numberOfSubdomains"] = config["compute"]["processors"]
            decompose_par_dict.writeFile()

        self._status = JobStatus.READY
        self._progress.save_job(self)

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
        if self._status == JobStatus.INITIALIZED:
            logger.info(
                f"Job {self._id} was initialized but not prepared, preparing and starting..."
            )
            self.prepare_job()

        if self._status == JobStatus.READY:
            logger.info(f"Job {self._id} is ready, starting...")

        if self._status == JobStatus.RUNNING:
            logger.info(
                f"Job {self._id} was previously running, cleaning up and restarting..."
            )
            # clean up

        if self._status == JobStatus.FAILED:
            logger.info(
                f"Job {self._id} previously fully ran but failed, restarting..."
            )

        if self._status == JobStatus.COMPLETE:
            logger.info(f"Job {self._id} already complete, skipping...")
            return None

        logger.info(
            f"======================= JOB {self._id} START ======================="
        )
        self._start_time = datetime.now()
        self._status = JobStatus.RUNNING
        self._progress.save_job(self)

        dispatch_ok = True

        # CREATE GEOMETRY ======================================================
        if should_create_geometry and dispatch_ok:
            start_time = datetime.now()
            try:
                logger.info(
                    f"Running create_geometry to generate a geometry for grid point {self._point.get_point_representation()}"
                )
                create_geometry_parameters = CreateGeometryParameters(
                    grid_point=self._point,
                    output_assets_directory=self._output_assets_directory,
                    job_id=self._id,
                    logger=logger,
                )
                create_geometry_return = create_geometry.create_geometry(
                    create_geometry_parameters=create_geometry_parameters
                )
                dispatch_ok = create_geometry_return.run_ok
                self._output_geometry_filepath = (
                    create_geometry_return.output_geometry_filepath
                )
                self._extra_variables = create_geometry_return.extra_variables
                logger.info("Successfully ran create_geometry")
            except BaseException:
                dispatch_ok = False
                logger.exception("An error occured in create_geometry")
            finally:
                end_time = datetime.now()
                self._steps.append(
                    Step(
                        id=StepId.CREATE_GEOMETRY,
                        run_ok=dispatch_ok,
                        start_time=start_time,
                        end_time=end_time,
                    )
                )
                self._progress.save_job(self)
        else:
            logger.warning("Skipping create_geometry")

        # MODIFY CASE ==========================================================
        if should_modify_case and dispatch_ok:
            start_time = datetime.now()
            try:
                logger.info("Running modify_case to customize OpenFOAM case")
                self._progress.save_job(self)
                modify_case_parameters = ModifyCaseParameters(
                    output_case_directory=self._output_case_directory,
                    job_id=self._id,
                    output_geometry_filepath=self._output_geometry_filepath,
                    logger=logger,
                    grid_point=self._point,
                    extra_variables=self._extra_variables,
                )
                modify_case_return = modify_case.modify_case(
                    modify_case_parameters=modify_case_parameters
                )
                dispatch_ok = modify_case_return.run_ok
                logger.info("Successfully ran modify_case")
            except BaseException:
                dispatch_ok = False
                logger.exception("An error occured in modify_case")
            finally:
                end_time = datetime.now()
                self._steps.append(
                    Step(
                        id=StepId.MODIFY_CASE,
                        run_ok=dispatch_ok,
                        start_time=start_time,
                        end_time=end_time,
                    )
                )
                self._progress.save_job(self)
        else:
            logger.warning("Skipping modify_case")

        # CREATE MESH ==========================================================
        if should_create_mesh and dispatch_ok:
            start_time = datetime.now()
            try:
                logger.info("Running create_mesh to generate a mesh for geometry")
                self._progress.save_job(self)
                create_mesh_parameters = CreateMeshParameters(
                    output_case_directory=self._output_case_directory,
                    job_id=self._id,
                    output_geometry_filepath=self._output_geometry_filepath,
                    logger=logger,
                )
                create_mesh_return = create_mesh.create_mesh(
                    create_mesh_parameters=create_mesh_parameters
                )
                dispatch_ok = create_mesh_return.run_ok
                logger.info("Successfully ran create_mesh")
            except BaseException:
                dispatch_ok = False
                logger.exception("An error occured in create_mesh")
            finally:
                end_time = datetime.now()
                self._steps.append(
                    Step(
                        id=StepId.CREATE_MESH,
                        run_ok=dispatch_ok,
                        start_time=start_time,
                        end_time=end_time,
                    )
                )
                self._progress.save_job(self)
        else:
            logger.warning("Skipping create_mesh")

        # EXECUTE SOLVER =======================================================
        if should_execute_solver and dispatch_ok:
            start_time = datetime.now()
            try:
                logger.info("Running execute_solver to obtain simulation results")
                self._progress.save_job(self)
                execute_solver_parameters = ExecuteSolverParameters(
                    output_case_directory=self._output_case_directory,
                    job_id=self._id,
                    logger=logger,
                )
                execute_solver_return = execute_solver.execute_solver(
                    execute_solver_parameters
                )
                dispatch_ok = execute_solver_return.run_ok
                logger.info("Successfully ran execute_solver")
            except BaseException:
                dispatch_ok = False
                logger.exception("An error occured in execute_solver")
            finally:
                end_time = datetime.now()
                self._steps.append(
                    Step(
                        id=StepId.EXECUTE_SOLVER,
                        run_ok=dispatch_ok,
                        start_time=start_time,
                        end_time=end_time,
                    )
                )
                self._progress.save_job(self)
        else:
            logger.warning("Skipping execute_solver")

        # EXTRACT OBJECTIVES ===================================================
        if should_extract_objectives and dispatch_ok:
            start_time = datetime.now()
            try:
                logger.info(
                    "Running extract_objectives for objective values extraction"
                )
                self._progress.save_job(self)
                extract_objectives_parameters = ExtractObjectivesParameters(
                    output_case_directory=self._output_case_directory,
                    job_id=self._id,
                    logger=logger,
                    objectives=get_config_objectives(),
                )
                extract_objectives_return = extract_objectives.extract_objectives(
                    extract_objectives_parameters=extract_objectives_parameters
                )
                dispatch_ok = extract_objectives_return.run_ok
                self._objectives = extract_objectives_return.objectives
                logger.info("Successfully ran extract_objectives")
            except BaseException:
                dispatch_ok = False
                logger.exception("An error occured in extract_objectives")
            finally:
                end_time = datetime.now()
                self._steps.append(
                    Step(
                        id=StepId.EXTRACT_OBJECTIVES,
                        run_ok=dispatch_ok,
                        start_time=start_time,
                        end_time=end_time,
                    )
                )
                self._progress.save_job(self)
        else:
            logger.warning("Skipping extract_objectives")

        # EXTRACT ASSETS =======================================================
        if should_extract_assets and dispatch_ok:
            start_time = datetime.now()
            try:
                logger.info("Running extract_assets for asset extraction")
                self._progress.save_job(self)
                extract_assets_parameters = ExtractAssetsParameters(
                    output_case_directory=self._output_case_directory,
                    output_case_foam_filepath=f"{self._output_case_directory}/{self._id}.foam",
                    output_assets_directory=self._output_assets_directory,
                    output_geometry_filepath=self._output_geometry_filepath,
                    job_id=self._id,
                    logger=logger,
                )
                extract_assets_return = extract_assets.extract_assets(
                    extract_assets_parameters=extract_assets_parameters
                )
                dispatch_ok = extract_assets_return.run_ok
                logger.info("Successfully ran extract_assets")
            except BaseException:
                logger.exception("An error occured in extract_assets")
                dispatch_ok = False
            finally:
                end_time = datetime.now()
                self._steps.append(
                    Step(
                        id=StepId.EXTRACT_ASSETS,
                        run_ok=dispatch_ok,
                        start_time=start_time,
                        end_time=end_time,
                    )
                )
                self._progress.save_job(self)
        else:
            logger.warning("Skipping extract_assets")

        # EXECUTE CLEANUP ======================================================
        # don't care about run_ok here, always cleanup regardless of whether run was ok or not
        cleanup_ok = True
        if should_execute_cleanup:
            start_time = datetime.now()
            try:
                logger.info("Running execute_cleanup for job cleanup")
                execute_cleanup_parameters = ExecuteCleanupParameters(
                    output_case_directory=self._output_case_directory,
                    job_id=self._id,
                    logger=logger,
                )
                execute_cleanup_return = execute_cleanup.execute_cleanup(
                    execute_cleanup_parameters=execute_cleanup_parameters
                )
                cleanup_ok = execute_cleanup_return.run_ok
                logger.info("Successfully ran execute_cleanup")
            except BaseException:
                cleanup_ok = False
                logger.exception("An error occured in execute_cleanup")
            finally:
                end_time = datetime.now()
                self._steps.append(
                    Step(
                        id=StepId.EXECUTE_CLEANUP,
                        run_ok=cleanup_ok,
                        start_time=start_time,
                        end_time=end_time,
                    )
                )
                self._progress.save_job(self)
        else:
            logger.warning("Skipping execute_cleanup")

        self._run_ok = dispatch_ok
        self._end_time = datetime.now()
        if dispatch_ok:
            self._status = JobStatus.COMPLETE
        else:
            objectives = get_config_objectives()
            for objective in objectives:
                objective.set_value(value=np.finfo(np.float64).max)
            self._objectives = objectives
            self._status = JobStatus.FAILED
        self._progress.save_job(self)

        logger.info(
            f"======================= JOB {self._id} END ========================="
        )

    def serialize(self):
        return {
            "id": self.get_id(),
            "status": self._status.value,
            "runOk": self._run_ok,
            "steps": [step.serialize() for step in self._steps],
            "startTime": self._start_time.isoformat(),
            "endTime": self._end_time.isoformat(),
            "outputGeometryFilepath": self._output_geometry_filepath,
            "outputCaseDirectory": self._output_case_directory,
            "outputAssetsDirectory": self._output_assets_directory,
            "point": self._point.serialize(),
            "objectives": [objective.serialize() for objective in self._objectives],
        }

    @classmethod
    def from_dict(cls, job: dict, progress: "Progress"):
        return cls(
            id=job["id"],
            point=Point.from_dict(point=job["point"]),
            progress=progress,
            steps=[Step.from_dict(step=step) for step in job["steps"]],
            status=JobStatus(value=job["status"]),
            run_ok=job["runOk"],
            start_time=datetime.fromisoformat(job["startTime"]),
            end_time=datetime.fromisoformat(job["endTime"]),
            output_geometry_filepath=job["outputGeometryFilepath"],
            output_case_directory=job["outputCaseDirectory"],
            output_assets_directory=job["outputAssetsDirectory"],
            objectives=[
                Objective.from_dict(objective=objective)
                for objective in job["objectives"]
            ],
        )
