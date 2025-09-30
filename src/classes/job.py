# system
import os
import sys
import tomllib

# visualization
import pyvista as pv

# logging
import logging
from logger.logger import LOGGER_NAME

# utils
from classes.point import Point

# OpenFOAM
from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory

# ==============================================================================

# config
with open("config.toml", "rb") as f:
    config = tomllib.load(f)

# logging
logger = logging.getLogger(LOGGER_NAME)

# FreeCAD module
FREECAD_PATH = config["model"]["freecad_path"]
sys.path.append(FREECAD_PATH)
import FreeCAD  # type: ignore  # noqa: E402
import Mesh  # type: ignore  # noqa: E402


class Job:
    _geometry_filepath = ""
    _case_filepath = ""

    def __init__(self, job_id: str, point: Point):
        self._job_id = job_id
        self._point = point

    def get_job_id(self):
        return self._job_id

    def generate_geometry(self):
        document = FreeCAD.open("input/model.FCStd")

        part = document.getObject("Body")

        spreadsheet = document.getObject("Spreadsheet")
        for variable in self._point.get_variables():
            cell = variable.get_cell()
            value = str(variable.get_value())
            spreadsheet.set(cell, value)

        # scaling - required for mm to m conversion (FreeCAD: STL in mm, OpenFOAM, STL in m)
        SCALE_FACTOR = config["model"]["scale_factor"]
        original_shape = part.Shape
        scaled_shape = original_shape.copy().scaled(
            SCALE_FACTOR, original_shape.CenterOfGravity
        )
        scaled_object = document.addObject("Part::Feature", self._job_id)
        scaled_object.Shape = scaled_shape

        document.recompute()

        GEOMETRIES_DIRECTORY = "output/geometries"
        os.makedirs(GEOMETRIES_DIRECTORY, exist_ok=True)
        OUTPUT_GEOMETRY_PATH = f"{GEOMETRIES_DIRECTORY}/{self._job_id}.stl"
        Mesh.export([scaled_object], OUTPUT_GEOMETRY_PATH)

        # probably don't need STEP files if we're going with snappHexMesh
        # part.Shape.exportStep(f"geometries/{i}.step")

        logger.info(
            f"Generated {self._job_id}.stl, volume: {scaled_shape.Volume}, area: {scaled_shape.Area}, design space: {self._point.get_point_representation()}"
        )

        self._geometry_filepath = OUTPUT_GEOMETRY_PATH

    def visualize_geometry(self):
        mesh = pv.read(self._geometry_filepath)
        mesh.plot()

    def create_case(self):
        CASES_DIRECTORY = "output/cases"
        os.makedirs(CASES_DIRECTORY, exist_ok=True)

        TEMPLATE_CASE_PATH = "input/template"
        OUTPUT_CASE_PATH = f"{CASES_DIRECTORY}/{self._job_id}"
        base_case = SolutionDirectory(TEMPLATE_CASE_PATH)
        copy_case = base_case.cloneCase(OUTPUT_CASE_PATH)

        logger.info(f"Generated case {copy_case.name} in {OUTPUT_CASE_PATH}")

        self._case_filepath = OUTPUT_CASE_PATH
