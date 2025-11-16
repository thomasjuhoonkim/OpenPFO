# system
import os
import shutil
import subprocess

# visualization
import pyvista as pv

# constants
from constants.modeler import AbstractModeler
from constants.path import (
    INPUT_CASE_TEMPLATE,
    OUTPUT_ASSETS_DIRECTORY,
    OUTPUT_CASES_DIRECTORY,
)

# classes
from classes.point import Point

# PyFOAM
from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory
from PyFoam.Execution.BasicRunner import BasicRunner

# input
from create_commands import create_commands
from modify_case import modify_case
from extract_assets import extract_assets
from extract_objectives import extract_objectives

# util
from util.get_cleanup_commands import get_cleanup_commands
from util.get_logger import get_logger

# ==============================================================================

# logging
logger = get_logger()


class Job:
    def __init__(self, job_id: str, point: Point, modeler: AbstractModeler):
        self._job_id = job_id
        self._point = point
        self._modeler = modeler

        self._output_geometry_filepath = ""
        self._output_case_directory = ""
        self._output_assets_directory = ""
        self._objective_values = None

    def get_job_id(self):
        return self._job_id

    def get_objective_values(self):
        return self._objective_values

    def prepare_geometry(self):
        self._output_geometry_filepath = self._modeler.generate_geometry(
            job_id=self._job_id, point=self._point
        )

    def visualize_geometry(self):
        mesh = pv.read(self._output_geometry_filepath)
        mesh.plot()

    def prepare_case(self):
        # copy case
        output_case_directory = f"{OUTPUT_CASES_DIRECTORY}/{self._job_id}"
        base_case = SolutionDirectory(INPUT_CASE_TEMPLATE)
        copy_case = base_case.cloneCase(output_case_directory)
        logger.info(f"Generated case {copy_case.name} in ./{output_case_directory}")

        # copy geometry into case trisurface directory
        trisurface_directory = f"{output_case_directory}/constant/triSurface"
        shutil.copy(self._output_geometry_filepath, trisurface_directory)
        os.rename(
            src=f"{trisurface_directory}/{self._job_id}.ast",
            dst=f"{trisurface_directory}/jobGeometry.stl",
        )
        logger.info(
            f"Copied geometry {self._output_geometry_filepath} into triSurface directory with name jobGeometry.stl"
        )

        self._output_case_directory = copy_case.name

    def prepare_assets(self):
        # create job assets directory
        output_assets_directory = f"{OUTPUT_ASSETS_DIRECTORY}/{self._job_id}"
        os.mkdir(output_assets_directory)
        self._output_assets_directory = output_assets_directory

    def dispatch(self):
        logger.info(
            f"======================= JOB {self._job_id} START ======================="
        )

        logger.info("Running modify_case to customize OpenFOAM case")
        modify_case(case_directory=self._output_case_directory, modeler=self._modeler)

        logger.info("Running OpenFOAM commands")
        user_commands = create_commands(case_directory=self._output_case_directory)
        for command in user_commands:
            runner = BasicRunner(argv=command.split(" "))
            runner.start()
            if not runner.runOK():
                logger.error(f"{command} failed")

        logger.info("Running extract_objectives for objective values extraction")
        self._objective_values = extract_objectives(
            case_directory=self._output_case_directory
        )

        logger.info("Running extract_assets for asset extraction")
        extract_assets(
            case_directory=self._output_case_directory,
            output_assets_directory=self._output_assets_directory,
        )

        logger.info("Starting cleanup")
        cleanup_commands = get_cleanup_commands(
            case_directory=self._output_case_directory
        )
        for command in cleanup_commands:
            try:
                result = subprocess.run(
                    command.split(" "), capture_output=True, text=True, check=True
                )
                logger.info(f"Output for command {command}: {result.stdout}")
            except subprocess.CalledProcessError as error:
                logger.error(f"{command} failed")
                logger.error(f"\n{error.stderr}")

        logger.info(
            f"======================= JOB {self._job_id} END ========================="
        )
