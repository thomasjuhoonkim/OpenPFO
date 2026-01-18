# classes
from classes.functions import ExecuteSolverParameters

# simple-slurm
from simple_slurm import Slurm


def execute_solver(
    execute_solver_parameters: ExecuteSolverParameters,
):
    """
    The execute_solver function is used to create the geometry for each grid
    point in the design space.

    NOTE: This function does not return a value.
    """

    """ ======================= YOUR CODE BELOW HERE ======================= """

    case_directory = execute_solver_parameters.output_case_directory
    logger = execute_solver_parameters.logger
    processors = execute_solver_parameters.processors

    slurm = Slurm(
        job_name="simpleFoam",
        account="def-jphickey",
        time="00:30:00",
        nodes=1,
        ntasks_per_node=processors,
        mem_per_cpu="4G",
        output="OpenPFO.log",
        open_mode="append",
    )
    slurm.set_wait(True)

    slurm.add_cmd(
        f"mpirun -np {processors} redistributePar -parallel -decompose -overwrite -case {case_directory}"
    )
    slurm.add_cmd(
        f"mpirun -np {processors} simpleFoam -parallel -case {case_directory}"
    )
    slurm.add_cmd(
        f"mpirun -np {processors} redistributePar -parallel -reconstruct -latestTime -case {case_directory}"
    )

    slurm_job_id = slurm.sbatch()
    logger.info(f"Successfully ran job {slurm_job_id} for simpleFoam.")

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return None
