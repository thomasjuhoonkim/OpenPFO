# system
import sys

# classes
from classes.point import Point

# constants
from constants.modeler import AbstractModeler
from constants.path import INPUT_DIRECTORY, OUTPUT_GEOMETRIES_DIRECTORY

# util
from util.get_config import get_config
from util.get_logger import get_logger

# ==============================================================================

config = get_config()
logger = get_logger()


class FreeCADModeler(AbstractModeler):
    def __init__(self):
        try:
            self._freecad_path = config["model"]["freecad_path"]
            sys.path.append(self._freecad_path)
            logger.info("FreeCAD path is defined")

            # FreeCAD module
            import FreeCAD  # type: ignore  # noqa: E402

            self._FreeCAD = FreeCAD
            logger.info("FreeCAD interface is valid")
        except Exception:
            logger.exception("An error occured while loading FreeCAD")
            sys.exit(1)

    def check_model(self):
        try:
            document = self._FreeCAD.open("input/model.FCStd")
            logger.info(f"FreeCAD Model found: {document.FileName}")

            part = document.getObject("Body")
            logger.info(f"FreeCAD Body found: {part.Name}")

        except Exception:
            logger.exception("An error occured while checking model")
            sys.exit(1)

    def generate_geometry(self, job_id: str, point: Point):
        import Mesh  # type: ignore # noqa: E402

        # Import Base Model
        document = self._FreeCAD.open(f"{INPUT_DIRECTORY}/model.FCStd")

        part = document.getObject("Body")

        # Design Space Interface
        spreadsheet = document.getObject("Spreadsheet")
        for variable in point.get_variables():
            cell = variable.get_cell()
            value = str(variable.get_value())
            spreadsheet.set(cell, value)

        export_object = document.addObject("Part::Feature", job_id)

        # scaling - required for mm to m conversion (FreeCAD: STL in mm, OpenFOAM, STL in m)
        SCALE_FACTOR = config["model"]["scale_factor"]
        original_shape = part.Shape
        scaled_shape = original_shape.copy().scaled(
            SCALE_FACTOR, self._FreeCAD.Vector(0, 0, 0)
        )
        export_object.Shape = scaled_shape
        logger.info(f"Scaled geometry {job_id} by {SCALE_FACTOR}")

        # Recompute Model
        document.recompute()

        # Export to STL
        output_geometry_filepath = f"{OUTPUT_GEOMETRIES_DIRECTORY}/{job_id}.ast"
        Mesh.export([export_object], output_geometry_filepath)

        logger.info(
            f"Generated {job_id}.stl, volume: {scaled_shape.Volume}, area: {scaled_shape.Area}, design variables: {point.get_point_representation()}"
        )

        return output_geometry_filepath


class OpenVSOModeler(AbstractModeler):
    def __init__(self):
        try:
            self._openvsp_path = config["model"]["openvsp_path"]
            sys.path.append(self._openvsp_path)
            logger.info("OpenVSP path is defined")

            # OpenVSP module
            import PyVSP as vsp  # type: ignore  # noqa: E402

            self._module = vsp
            logger.info("OpenVSP interface is valid")
        except Exception:
            logger.exception("An error occured while loading OpenVSP")
            sys.exit(1)

    def check_model(self):
        try:
            vsp = self._module

            vsp.ReadVSPFile("input/model.vsp3")
            logger.info(f"OpenVSP Model found: {vsp.GetVSPFileName()}")

            vehicle_id = vsp.getVehicleId()
            logger.info(f"OpenVSP Vehicle found: {vehicle_id}")

        except Exception:
            logger.exception("An error occured while checking model")
            sys.exit(1)

    def generate_geometry(self, job_id: str, point: Point):
        pass
