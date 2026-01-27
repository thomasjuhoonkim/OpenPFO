# classes
from classes.functions import CreateMeshParameters, CreateMeshReturn

# PyFoam
from PyFoam.Execution.BasicRunner import BasicRunner


def create_mesh(
    create_mesh_parameters: CreateMeshParameters,
):
    """
    The create_mesh function is used to create the geometry for each grid
    point in the design space.
    """

    """ ======================= YOUR CODE BELOW HERE ======================= """

    case_directory = create_mesh_parameters.output_case_directory
    logger = create_mesh_parameters.logger
    commands = [
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

    CREATE_MESH_RETURN = CreateMeshReturn()

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return CREATE_MESH_RETURN
