# system
import os

# datetime
from datetime import datetime

# threading
import threading

# typing
from typing import TYPE_CHECKING

# constants
from constants.path import OUTPUT_DIRECTORY
from constants.job import JobStatus
from constants.step import StepId
from classes.meta import Meta

# classes
if TYPE_CHECKING:
    from classes.progress import Progress
from classes.functions import (
    PrepareParameters,
    GeometryParameters,
    MeshParameters,
    SolveParameters,
    ObjectivesParameters,
    CleanupParameters,
)
from classes.objective import Objective
from classes.point import Point
from classes.step import Step

# util
from util.get_config_objectives import get_config_objectives
from util.get_config import get_config
from util.get_logger import get_logger

# input
prepare = __import__("0_prepare")
geometry = __import__("1_geometry")
mesh = __import__("2_mesh")
solve = __import__("3_solve")
objectives = __import__("4_objectives")
cleanup = __import__("5_cleanup")

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
        search_id="",
        steps: list["Step"] | None = None,
        status: JobStatus | None = None,
        run_ok=True,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        job_directory="",
        objectives: list["Objective"] | None = None,
        meta: "Meta" = None,
    ):
        self._id = id
        self._point = point
        self._search_id = search_id
        self._progress = progress
        self._steps = steps if steps is not None else []
        self._status = status if status is not None else JobStatus.READY
        self._run_ok = run_ok
        self._start_time = start_time if start_time is not None else datetime.now()
        self._end_time = end_time if end_time is not None else datetime.now()
        self._visualize_filepath = ""
        self._job_directory = (
            job_directory if job_directory else f"{OUTPUT_DIRECTORY}/{id}"
        )
        self._objectives = objectives if objectives is not None else []
        self._meta = Meta() if meta is None else meta

        if not os.path.isdir(self._job_directory):
            os.makedirs(self._job_directory)
            logger.info(f"Created job directory {self._job_directory}")

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

    def get_job_directory(self):
        return self._job_directory

    def get_point(self):
        return self._point

    def get_objectives(self):
        return self._objectives

    def get_meta(self):
        return self._meta

    def visualize_geometry(self):
        if IS_HPC:
            logger.warning(
                "config.compute.hpc is set true, geometry visualization with PyVista is unavailable."
            )
            return None
        if not self._visualize_filepath:
            logger.error(
                "No visualize_filepath configured, double check that you return a geometry filepath in geometry()"
            )
            return None

        mesh = pv.read(self._visualize_filepath)
        mesh.plot(window_size=[1920, 1080])

    def dispatch(
        self,
        should_run_checks=True,
        should_run_prepare=True,
        should_run_geometry=True,
        should_run_mesh=True,
        should_run_solve=True,
        should_run_objectives=True,
        should_run_cleanup=True,
        lock=threading.Lock(),
    ):
        if should_run_checks:
            if self._status == JobStatus.READY:
                logger.info(f"Job {self._id} is ready, starting...")

            if self._status == JobStatus.RUNNING:
                logger.info(
                    f"Job {self._id} was previously running, cleaning up and restarting..."
                )
                self.cleanup(lock=lock)

            if self._status == JobStatus.FAILED:
                logger.info(f"Job {self._id} previously failed, skipping...")
                return None

            if self._status == JobStatus.COMPLETE:
                logger.info(f"Job {self._id} already complete, skipping...")
                return None

        logger.info(
            f"======================= JOB {self._id} START ======================="
        )
        self._start_time = datetime.now()
        self._status = JobStatus.RUNNING
        with lock:
            self._progress.save_job(self)

        dispatch_ok = True

        # PREPARE ==============================================================
        if should_run_prepare and dispatch_ok:
            start_time = datetime.now()
            try:
                logger.info(f"Running prepare() for {self._id}")
                prepare_parameters = PrepareParameters(
                    job_directory=self._job_directory,
                    point=self._point,
                    meta=self._meta,
                    job_id=self._id,
                    logger=logger,
                )
                prepare_return = prepare.prepare(prepare_parameters=prepare_parameters)
                dispatch_ok = prepare_return.run_ok
                logger.info(f"Successfully ran prepare() for job {self._id}")
            except BaseException:
                dispatch_ok = False
                logger.exception(
                    f"An error occured while running prepare() for job {self._id}"
                )
            finally:
                end_time = datetime.now()
                self._steps.append(
                    Step(
                        id=StepId.PREPARE,
                        run_ok=dispatch_ok,
                        start_time=start_time,
                        end_time=end_time,
                    )
                )
                with lock:
                    self._progress.save_job(self)
        else:
            logger.warning(f"Skipping prepare() for job {self._id}")

        # GEOMETRY =============================================================
        if should_run_geometry and dispatch_ok:
            start_time = datetime.now()
            try:
                logger.info(f"Running geometry() for job {self._id}")
                geometry_parameters = GeometryParameters(
                    job_directory=self._job_directory,
                    point=self._point,
                    meta=self._meta,
                    job_id=self._id,
                    logger=logger,
                )
                geometry_return = geometry.geometry(
                    geometry_parameters=geometry_parameters
                )
                dispatch_ok = geometry_return.run_ok
                self._visualize_filepath = geometry_return.visualize_filepath
                logger.info(f"Successfully ran geometry() for job {self._id}")
            except BaseException:
                dispatch_ok = False
                logger.exception(
                    f"An error occured while running geometry() for job {self._id}"
                )
            finally:
                end_time = datetime.now()
                self._steps.append(
                    Step(
                        id=StepId.GEOMETRY,
                        run_ok=dispatch_ok,
                        start_time=start_time,
                        end_time=end_time,
                    )
                )
                with lock:
                    self._progress.save_job(self)
        else:
            logger.warning(f"Skipping geometry() for job {self._id}")

        # MESH =================================================================
        if should_run_mesh and dispatch_ok:
            start_time = datetime.now()
            try:
                logger.info(f"Running mesh() for {self._id}")
                mesh_parameters = MeshParameters(
                    job_directory=self._job_directory,
                    point=self._point,
                    meta=self._meta,
                    job_id=self._id,
                    logger=logger,
                )
                mesh_return = mesh.mesh(mesh_parameters=mesh_parameters)
                dispatch_ok = mesh_return.run_ok
                logger.info(f"Successfully ran mesh() for job {self._id}")
            except BaseException:
                dispatch_ok = False
                logger.exception(
                    f"An error occured while running mesh() for job {self._id}"
                )
            finally:
                end_time = datetime.now()
                self._steps.append(
                    Step(
                        id=StepId.MESH,
                        run_ok=dispatch_ok,
                        start_time=start_time,
                        end_time=end_time,
                    )
                )
                with lock:
                    self._progress.save_job(self)
        else:
            logger.warning(f"Skipping mesh() for job {self._id}")

        # SOLVE ================================================================
        if should_run_solve and dispatch_ok:
            start_time = datetime.now()
            try:
                logger.info(f"Running solve() for job {self._id}")
                solve_parameters = SolveParameters(
                    job_directory=self._job_directory,
                    point=self._point,
                    meta=self._meta,
                    job_id=self._id,
                    logger=logger,
                )
                solve_return = solve.solve(solve_parameters=solve_parameters)
                dispatch_ok = solve_return.run_ok
                logger.info(f"Running solve() for job {self._id}")
            except BaseException:
                dispatch_ok = False
                logger.exception(
                    f"An error occured while running solve() for job {self._id}"
                )
            finally:
                end_time = datetime.now()
                self._steps.append(
                    Step(
                        id=StepId.SOLVE,
                        run_ok=dispatch_ok,
                        start_time=start_time,
                        end_time=end_time,
                    )
                )
                with lock:
                    self._progress.save_job(self)
        else:
            logger.warning(f"Skipping solve() for job {self._id}")

        # OBJECTIVES ===========================================================
        if should_run_objectives and dispatch_ok:
            start_time = datetime.now()
            try:
                logger.info(f"Running objectives() for {self._id}")
                objectives_parameters = ObjectivesParameters(
                    objectives=get_config_objectives(),
                    job_directory=self._job_directory,
                    point=self._point,
                    meta=self._meta,
                    job_id=self._id,
                    logger=logger,
                )
                objectives_return = objectives.objectives(
                    objectives_parameters=objectives_parameters
                )
                dispatch_ok = objectives_return.run_ok
                self._objectives = objectives_return.objectives
                logger.info(f"Successfully ran objectives() for job {self._id}")
            except BaseException:
                dispatch_ok = False
                logger.exception(
                    f"An error occured while running objectives() for job {self._id}"
                )
            finally:
                end_time = datetime.now()
                self._steps.append(
                    Step(
                        id=StepId.OBJECTIVES,
                        run_ok=dispatch_ok,
                        start_time=start_time,
                        end_time=end_time,
                    )
                )
                with lock:
                    self._progress.save_job(self)
        else:
            logger.warning(f"Skipping objectives() for job {self._id}")

        # CLEANUP ==============================================================
        # don't care about run_ok here, always cleanup regardless of whether run was ok or not
        # we create a separate clean_ok here to check the status of cleanup specifically
        if should_run_cleanup:
            self.cleanup(lock=lock)
        else:
            logger.warning(f"Skipping cleanup() for job {self._id}")

        self._run_ok = dispatch_ok
        self._end_time = datetime.now()
        if dispatch_ok:
            self._status = JobStatus.COMPLETE
        else:
            self._objectives = get_config_objectives()
            self._status = JobStatus.FAILED
        with lock:
            self._progress.save_job(self)

        logger.info(
            f"======================= JOB {self._id} END ========================="
        )

    def cleanup(self, lock=threading.Lock()):
        start_time = datetime.now()
        cleanup_ok = True
        try:
            logger.info(f"Running cleanup() for job {self._id}")
            cleanup_parameters = CleanupParameters(
                job_directory=self._job_directory,
                point=self._point,
                meta=self._meta,
                job_id=self._id,
                logger=logger,
            )
            cleanup_return = cleanup.cleanup(cleanup_parameters=cleanup_parameters)
            cleanup_ok = cleanup_return.run_ok
            logger.info(f"Successfully ran cleanup() for job {self._id}")
        except BaseException:
            cleanup_ok = False
            logger.exception(
                f"An error occured while running cleanup() for job {self._id}"
            )
        finally:
            end_time = datetime.now()
            self._steps.append(
                Step(
                    id=StepId.CLEANUP,
                    run_ok=cleanup_ok,
                    start_time=start_time,
                    end_time=end_time,
                )
            )
            with lock:
                self._progress.save_job(self)

    def serialize(self):
        return {
            "id": self.get_id(),
            "searchId": self._search_id,
            "status": self._status.value,
            "runOk": self._run_ok,
            "steps": [step.serialize() for step in self._steps],
            "startTime": self._start_time.isoformat(),
            "endTime": self._end_time.isoformat(),
            "jobDirectory": self._job_directory,
            "point": self._point.serialize(),
            "objectives": [objective.serialize() for objective in self._objectives],
            "meta": self._meta.serialize(),
        }

    @classmethod
    def from_dict(cls, job: dict, progress: "Progress"):
        return cls(
            id=job["id"],
            point=Point.from_dict(point=job["point"]),
            search_id=job["searchId"],
            progress=progress,
            steps=[Step.from_dict(step=step) for step in job["steps"]],
            status=JobStatus(value=job["status"]),
            run_ok=job["runOk"],
            start_time=datetime.fromisoformat(job["startTime"]),
            end_time=datetime.fromisoformat(job["endTime"]),
            job_directory=job["jobDirectory"],
            objectives=[
                Objective.from_dict(objective=objective)
                for objective in job["objectives"]
            ],
            meta=Meta.from_dict(job["meta"]),
        )
