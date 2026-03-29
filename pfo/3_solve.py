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
        f"mpirun -np {processors_per_job} rhoCentralFoam -parallel -case {job_directory}",
        f"mpirun -np {processors_per_job} redistributePar -parallel -reconstruct -latestTime -case {job_directory}",
    ]

    slurm = Slurm(
        job_name=f"{job_id}-rhoCentralFoam",
        account="def-jphickey",
        time="04:00:00",
        nodes=1,
        ntasks_per_node=processors_per_job,
        mem_per_cpu="1G",
        output=f"{job_directory}/rhoCentralFoam.log",
        open_mode="append",
    )
    slurm.set_wait(True)

    for command in COMMANDS:
        slurm.add_cmd(command)

    slurm.sbatch()

    # VALIDATION ===============================================================

    run_ok = True
    if not os.path.isdir(f"{job_directory}/0.5"):
        run_ok = False

    SOLVE_RETURN = SolveReturn(run_ok=run_ok)

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return SOLVE_RETURN
