# system
import os
import sys
import subprocess

# classes
from classes.point import Point

# constants
from constants.modeler import AbstractModeler

# util
from util.get_config import get_config
from util.get_logger import get_logger

# ==============================================================================

config = get_config()
logger = get_logger()


class FreeCADModeler(AbstractModeler):
    def __init__(self, model_filepath: str, freecad_filepath: str):
        try:
            self._model_filepath = model_filepath
            self._freecad_filepath = freecad_filepath
            sys.path.append(self._freecad_filepath)
            logger.info("FreeCAD path is defined")

            # FreeCAD module
            import FreeCAD  # type: ignore  # noqa: E402

            FreeCAD.Version()
            logger.info("FreeCAD interface is valid")
        except Exception:
            logger.exception("An error occured while loading FreeCAD")
            sys.exit(1)

    def check_model(self):
        try:
            import FreeCAD  # type: ignore  # noqa: E402

            document = FreeCAD.open(self._model_filepath)
            logger.info(f"FreeCAD Model found: {document.FileName}")

            part = document.getObject("Body")
            logger.info(f"FreeCAD Body found: {part.Name}")

        except Exception:
            logger.exception("An error occured while checking the model")
            sys.exit(1)

    def generate_geometry(
        self,
        job_id: str,
        point: Point,
        output_assets_directory: str,
    ):
        import FreeCAD  # type: ignore  # noqa: E402
        import Mesh  # type: ignore # noqa: E402

        # Import Base Model
        document = FreeCAD.open(self._model_filepath)

        part = document.getObject("Body")

        # Design Space Interface
        spreadsheet = document.getObject("Spreadsheet")
        for variable in point.get_variables():
            cell = variable.get_id()
            value = str(variable.get_value())
            spreadsheet.set(cell, value)

        # Recompute Model
        document.recompute()

        # Export to AST
        output_ast = f"{output_assets_directory}/{job_id}.ast"
        output_stl = f"{output_assets_directory}/{job_id}.stl"
        Mesh.export([part], output_ast)

        # rename AST to STL
        os.rename(src=output_ast, dst=output_stl)
        output_geometry_filepath = output_stl

        logger.info(
            f"Generated {job_id}.stl, volume: {part.Shape.Volume}, area: {part.Shape.Area}, design variables: {point.get_point_representation()}"
        )

        return output_geometry_filepath


class OpenVSPModeler(AbstractModeler):
    def __init__(self, model_filepath: str, openvsp_filepath: str):
        self._model_filepath = model_filepath
        self._openvsp_filepath = openvsp_filepath
        if os.path.exists(openvsp_filepath):
            logger.info("OpenVSP filepath exists")
        else:
            logger.error("OpenVSP filepath does not exist")
            sys.exit(1)

        # OpenVSP module
        try:
            subprocess.run([openvsp_filepath])
            logger.info("OpenVSP interface is valid")
        except subprocess.CalledProcessError as error:
            logger.error(f"An error occured while loading OpenVSP: {error.stdout}")
            sys.exit(1)

    def check_model(self):
        try:
            subprocess.run([self._openvsp_filepath, self._model_filepath])
            logger.info("OpenVSP model is valid")
        except subprocess.CalledProcessError as error:
            logger.error(
                f"An error occured while loading OpenVSP model: {error.stdout}"
            )
            sys.exit(1)

    def generate_geometry(
        self, job_id: str, point: Point, output_assets_directory: str
    ):
        # design variables file for openvsp model variable definitions
        design_variables_filepath = f"{output_assets_directory}/{job_id}.des"
        variables = point.get_variables()
        variables_definitions = ""

        for variable in variables:
            id = variable.get_id()
            value = variable.get_value()
            variables_definitions += f"{id}: {value}\n"
        design_variables_content = f"""{len(variables)}\n{variables_definitions}"""

        with open(design_variables_filepath, "w") as f:
            f.write(design_variables_content)

        # vspscript file for vsp model mutation
        output_geometry_filepath = f"{output_assets_directory}/{job_id}.stl"
        vspscript_filepath = f"{output_assets_directory}/{job_id}.vspscript"
        vspscript_content = f"""
void main()
{{
    ClearVSPModel();
    ReadVSPFile("{self._model_filepath}");
    Update();
    ReadApplyDESFile("{design_variables_filepath}");
    Update();
    ExportFile("{output_geometry_filepath}", SET_ALL, EXPORT_STL);
    VSPExit(0);
}}
"""

        with open(vspscript_filepath, "w") as f:
            f.write(vspscript_content)

        # cli commands for openvsp
        command = [
            self._openvsp_filepath,
            "-script",
            vspscript_filepath,
        ]

        try:
            subprocess.run(command, capture_output=True, text=True, check=True)
            logger.info(
                f"Generated {output_geometry_filepath}, design variables: {point.get_point_representation()}"
            )
        except subprocess.CalledProcessError as error:
            logger.error(f"{' '.join(command)} failed")
            logger.error(f"\n{error.stdout}")

        return output_geometry_filepath
