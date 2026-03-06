# system
import os

# classes
from classes.functions import SolveParameters, SolveReturn

# simple-slurm
from simple_slurm import Slurm


def solve(
    solve_parameters: SolveParameters,
):
    """
    This function is used to solve the mesh for each point in the design space.
    """

    job_directory = solve_parameters.job_directory
    processors_per_job = solve_parameters.processors_per_job
    job_id = solve_parameters.job_id
    logger = solve_parameters.logger
    point = solve_parameters.point
    meta = solve_parameters.meta

    """ ======================= YOUR CODE BELOW HERE ======================= """

    COMMANDS = [
        f"mpirun -np {processors_per_job} redistributePar -parallel -decompose -overwrite -case {job_directory}",
        f"mpirun -np {processors_per_job} simpleFoam -parallel -case {job_directory}",
        f"mpirun -np {processors_per_job} redistributePar -parallel -reconstruct -latestTime -case {job_directory}",
    ]

    slurm = Slurm(
        job_name=f"{job_id}-simpleFoam",
        account="def-jphickey",
        time="02:15:00",
        nodes=1,
        ntasks_per_node=processors_per_job,
        mem_per_cpu="4G",
        output=f"{job_directory}/simpleFoam.log",
        open_mode="append",
    )
    slurm.set_wait(True)

    for command in COMMANDS:
        slurm.add_cmd(command)

    slurm.sbatch()

    # VALIDATION ===============================================================

    run_ok = True
    if not os.path.isdir(f"{job_directory}/40"):
        run_ok = False

    SOLVE_RETURN = SolveReturn(run_ok=run_ok)

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return SOLVE_RETURN
