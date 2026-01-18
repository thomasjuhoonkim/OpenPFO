# classes
from classes.functions import CreateMeshParameters

# util
from util.get_config import get_config

# PyFoam
from PyFoam.Execution.BasicRunner import BasicRunner


config = get_config()

PROCESSORS = config["compute"]["processors"]


def create_mesh(
    create_mesh_parameters: CreateMeshParameters,
):
    """
    The create_mesh function is used to create the geometry for each grid
    point in the design space.

    NOTE: This function does not return a value.
    """

    """ ======================= YOUR CODE BELOW HERE ======================= """

    case_directory = create_mesh_parameters.output_case_directory
    logger = create_mesh_parameters.logger
    commands = [
        # f"blockMesh -case {case_directory}",
        # f"surfaceTransformPoints -case {case_directory} -scale 0.001 {geometry_filepath} {case_directory}/constant/triSurface/jobGeometry.stl",
        # f"surfaceFeatureExtract -case {case_directory}",
        # f"mpirun -np {PROCESSORS} redistributePar -parallel -decompose -overwrite -case {case_directory}",
        # f"mpirun -np {PROCESSORS} snappyHexMesh -parallel -overwrite -case {case_directory}",
        # f"mpirun -np {PROCESSORS} redistributePar -parallel -reconstruct -overwrite -constant -case {case_directory}",
        # =====================================================================================================================================
        f"surfaceTransformPoints -case {case_directory} -rotate-angle '((0 1 0) 5)' {case_directory}/original.stl {case_directory}/aoa.stl",
        f"surfaceGenerateBoundingBox -case {case_directory} {case_directory}/aoa.stl {case_directory}/combined.stl 50 50 25 25 10 10",
        f"surfaceFeatureEdges {case_directory}/combined.stl {case_directory}/combined.fms -angle 5 -case {case_directory}",
        f"cartesianMesh -case {case_directory}",
    ]

    for command in commands:
        runner = BasicRunner(argv=command.split(" "))
        runner.start()
        if not runner.runOK():
            logger.error(f"{command} failed")
            raise Exception(f"{command} failed")

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return None
