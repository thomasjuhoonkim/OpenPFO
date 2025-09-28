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
from util.point import Point

# OpenFOAM
import casefoam

GEOMETRIES_DIRECTORY = "output/geometries"

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

    def __init__(self, job_id: str, point: Point):
        self._job_id = job_id
        self._point = point

    def get_job_id(self):
        return self._job_id

    def generate_geometry(self):
        document = FreeCAD.open("input/model.FCStd")

        spreadsheet = document.getObject("Spreadsheet")
        for variable in self._point.get_variables():
            cell = variable.get_cell()
            value = str(variable.get_value())
            spreadsheet.set(cell, value)

        document.recompute()
        part = document.getObject("Body")
        os.makedirs(GEOMETRIES_DIRECTORY, exist_ok=True)
        filepath = f"{GEOMETRIES_DIRECTORY}/{self._job_id}.stl"
        Mesh.export([part], filepath)

        # probably don't need STEP files if we're going with snappHexMesh
        # part.Shape.exportStep(f"geometries/{i}.step")

        logger.info(
            f"Generated {self._job_id}.stl, volume: {part.Shape.Volume}, area: {part.Shape.Area}, design space: {self._point.get_point_representation()}"
        )

        self._geometry_filepath = filepath

    def visualize_geometry(self):
        mesh = pv.read(self._geometry_filepath)
        mesh.plot()

    def create_case(self):
        pass
