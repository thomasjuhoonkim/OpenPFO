# system
import os

# classes
from classes.functions import MeshParameters, MeshReturn

# # simple-slurm
# from simple_slurm import Slurm

# PyFoam
from PyFoam.Execution.BasicRunner import BasicRunner


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
    meta = mesh_parameters.meta

    """ ======================= YOUR CODE BELOW HERE ======================= """

    COMMANDS = [
        f"blockMesh -case {job_directory}",
    ]

    for command in COMMANDS:
        runner = BasicRunner(argv=command.split(" "))
        runner.start()
        if not runner.runOK():
            logger.error(f"{command} failed")
            raise Exception(f"{command} failed")

    # slurm = Slurm(
    #     job_name=f"{job_id}-blockMesh",
    #     account="def-jphickey",
    #     time="00:10:00",
    #     nodes=1,
    #     ntasks_per_node=1,
    #     cpus_per_task=processors_per_job,
    #     mem="32G",
    #     output=f"{job_directory}/blockMesh.log",
    #     open_mode="append",
    # )
    # slurm.set_wait(True)

    # for command in COMMANDS:
    #     slurm.add_cmd(command)

    # slurm.sbatch()

    # VALIDATION ===============================================================

    run_ok = True
    if not os.path.isdir(f"{job_directory}/constant/polyMesh"):
        run_ok = False

    MESH_RETURN = MeshReturn(run_ok=run_ok)

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return MESH_RETURN
