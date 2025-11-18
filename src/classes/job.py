# system
import os

# visualization
import pyvista as pv

# constants
from classes.functions import (
    CreateGeometryParameters,
    CreateMeshParameters,
    ExecuteCleanupParameters,
    ExecuteSolverParameters,
    ExtractAssetsParameters,
    ExtractObjectivesParameters,
    ModifyCaseParameters,
)
from constants.path import (
    INPUT_CASE_TEMPLATE,
    OUTPUT_ASSETS_DIRECTORY,
    OUTPUT_CASES_DIRECTORY,
)

# classes
from classes.point import Point

# PyFOAM
from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory

# input
from create_geometry import create_geometry
from create_mesh import create_mesh
from execute_cleanup import execute_cleanup
from execute_solver import execute_solver
from modify_case import modify_case
from extract_assets import extract_assets
from extract_objectives import extract_objectives

# util
from util.get_logger import get_logger

# ==============================================================================

# logging
logger = get_logger()


class Job:
    def __init__(self, job_id: str, point: Point):
        self._job_id = job_id
        self._point = point

        self._output_geometry_filepath = ""
        self._output_case_directory = ""
        self._output_assets_directory = ""
        self._objective_values = None

    def get_objective_values(self):
        return self._objective_values

    def visualize_geometry(self):
        mesh = pv.read(self._output_geometry_filepath)
        mesh.plot(window_size=[1920, 1080])

    def prepare_job(
        self, should_create_assets_directory=True, should_create_case_directory=True
    ):
        if should_create_assets_directory:
            # create job assets directory
            output_assets_directory = f"{OUTPUT_ASSETS_DIRECTORY}/{self._job_id}"
            os.mkdir(output_assets_directory)
            self._output_assets_directory = output_assets_directory
            logger.info(f"Created assets directory {output_assets_directory}")

        if should_create_case_directory:
            # copy case
            output_case_directory = f"{OUTPUT_CASES_DIRECTORY}/{self._job_id}"
            base_case = SolutionDirectory(INPUT_CASE_TEMPLATE)
            copy_case = base_case.cloneCase(output_case_directory)
            self._output_case_directory = copy_case.name
            logger.info(f"Generated case directory {copy_case.name}")

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

        if should_create_geometry:
            logger.info(
                f"Running create_geometry to generate a geometry for grid point {self._point.get_point_representation()}"
            )
            create_geometry_parameters = CreateGeometryParameters(
                grid_point=self._point,
                output_assets_directory=self._output_assets_directory,
                job_id=self._job_id,
                logger=logger,
            )
            create_geometry_return = create_geometry(
                create_geometry_parameters=create_geometry_parameters
            )
            self._output_geometry_filepath = (
                create_geometry_return.output_geometry_filepath
            )

        if should_modify_case:
            logger.info("Running modify_case to customize OpenFOAM case")
            modify_case_parameters = ModifyCaseParameters(
                output_case_directory=self._output_case_directory,
                job_id=self._job_id,
                output_geometry_filepath=self._output_geometry_filepath,
                logger=logger,
            )
            modify_case(modify_case_parameters=modify_case_parameters)

        if should_create_mesh:
            logger.info("Running create_mesh to generate a mesh for geometry")
            create_mesh_parameters = CreateMeshParameters(
                output_case_directory=self._output_case_directory,
                job_id=self._job_id,
                output_geometry_filepath=self._output_geometry_filepath,
                logger=logger,
            )
            create_mesh(create_mesh_parameters=create_mesh_parameters)

        if should_execute_solver:
            logger.info("Running execute_solver to obtain simulation results")
            execute_solver_parameters = ExecuteSolverParameters(
                output_case_directory=self._output_case_directory, job_id=self._job_id
            )
            execute_solver(execute_solver_parameters)

        if should_extract_objectives:
            logger.info("Running extract_objectives for objective values extraction")
            extract_objectives_parameters = ExtractObjectivesParameters(
                output_case_directory=self._output_case_directory, job_id=self._job_id
            )
            extract_objectives_return = extract_objectives(
                extract_objectives_parameters=extract_objectives_parameters
            )
            self._objective_values = extract_objectives_return.objectives

        if should_extract_assets:
            logger.info("Running extract_assets for asset extraction")
            extract_assets_parameters = ExtractAssetsParameters(
                output_case_directory=self._output_case_directory,
                output_case_foam_filepath=f"{self._output_case_directory}/{self._job_id}.foam",
                output_assets_directory=self._output_assets_directory,
                output_geometry_filepath=self._output_geometry_filepath,
                job_id=self._job_id,
                logger=logger,
            )
            extract_assets(extract_assets_parameters=extract_assets_parameters)

        if should_execute_cleanup:
            logger.info("Running execute_cleanup for job cleanup")
            execute_cleanup_parameters = ExecuteCleanupParameters(
                output_case_directory=self._output_case_directory,
                job_id=self._job_id,
                logger=logger,
            )
            execute_cleanup(execute_cleanup_parameters=execute_cleanup_parameters)

        logger.info(
            f"======================= JOB {self._job_id} END ========================="
        )
