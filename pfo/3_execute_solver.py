# system
import os

# classes
from classes.functions import ExecuteSolverParameters, ExecuteSolverReturn

# simple-slurm
from simple_slurm import Slurm


def execute_solver(
    execute_solver_parameters: ExecuteSolverParameters,
):
    """
    The execute_solver function is used to create the geometry for each grid
    point in the design space.
    """

    """ ======================= YOUR CODE BELOW HERE ======================= """

    case_directory = execute_solver_parameters.output_case_directory
    logger = execute_solver_parameters.logger
    processors_per_job = execute_solver_parameters.processors_per_job

    slurm = Slurm(
        job_name="simpleFoam",
        account="def-jphickey",
        time="01:00:00",
        nodes=1,
        ntasks_per_node=processors_per_job,
        threads_per_core=1,
        mem_per_cpu="4G",
        output=f"{case_directory}/simpleFoam.log",
        open_mode="append",
    )
    slurm.set_wait(True)

    slurm.add_cmd(
        f"mpirun -np {processors_per_job} redistributePar -parallel -decompose -case {case_directory}"
    )
    slurm.add_cmd(
        f"mpirun -np {processors_per_job} simpleFoam -parallel -case {case_directory}"
    )
    slurm.add_cmd(
        f"mpirun -np {processors_per_job} redistributePar -parallel -reconstruct -latestTime -case {case_directory}"
    )

    slurm.sbatch()
    logger.info("Successfully ran simpleFoam.")

    run_ok = True
    if not os.path.isdir(f"{case_directory}/20"):
        run_ok = False

    EXECUTE_SOLVER_RETURN = ExecuteSolverReturn(run_ok=run_ok)

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return EXECUTE_SOLVER_RETURN
