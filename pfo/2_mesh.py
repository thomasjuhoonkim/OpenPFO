# system
import os

# classes
from classes.functions import MeshParameters, MeshReturn

# PyFoam
from PyFoam.Execution.BasicRunner import BasicRunner

# simple-slurm
from simple_slurm import Slurm


def mesh(
    mesh_parameters: MeshParameters,
):
    """
    The function is used to generate a mesh for each point in the design space.
    """

    job_directory = mesh_parameters.job_directory
    processors_per_job = mesh_parameters.processors_per_job
    logger = mesh_parameters.logger
    job_id = mesh_parameters.job_id
    point = mesh_parameters.point

    """ ======================= YOUR CODE BELOW HERE ======================= """

    COMMANDS = [
        f"surfaceTransformPoints -case {job_directory} -rotate-angle '((0 1 0) 5)' {job_directory}/{job_id}.stl {job_directory}/aoa.stl",
        f"surfaceGenerateBoundingBox -case {job_directory} {job_directory}/aoa.stl {job_directory}/combined.stl 50 50 25 25 10 10",
        f"surfaceFeatureEdges {job_directory}/combined.stl {job_directory}/combined.fms -angle 5 -case {job_directory}",
        f"cartesianMesh -case {job_directory}",
    ]

    # for command in COMMANDS:
    #     runner = BasicRunner(argv=command.split(" "))
    #     runner.start()
    #     if not runner.runOK():
    #         logger.error(f"{command} failed")
    #         raise Exception(f"{command} failed")

    slurm = Slurm(
        job_name=f"{job_id}-cartesianMesh",
        account="def-jphickey",
        time="00:05:00",
        nodes=1,
        ntasks_per_node=1,
        cpus_per_task=processors_per_job,
        mem="16G",
        output=f"{job_directory}/cartesianMesh.log",
        open_mode="append",
    )
    slurm.set_wait(True)

    for command in COMMANDS:
        slurm.add_cmd(command)

    slurm.sbatch()

    # VALIDATION ===============================================================

    run_ok = True
    if not os.path.isdir(f"{job_directory}/constant/polyMesh"):
        run_ok = False

    MESH_RETURN = MeshReturn(run_ok=run_ok)

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return MESH_RETURN
