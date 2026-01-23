# classes
from classes.functions import ExecuteCleanupParameters, ExecuteCleanupReturn

# simple-slurm
from simple_slurm import Slurm


def execute_cleanup(
    execute_cleanup_parameters: ExecuteCleanupParameters,
):
    """
    The execute_cleanup function used to clean up solver artifacts after each job.
    """

    """ ======================= YOUR CODE BELOW HERE ======================= """

    case_directory = execute_cleanup_parameters.output_case_directory
    logger = execute_cleanup_parameters.logger
    processors_per_job = execute_cleanup_parameters.processors_per_job

    slurm1 = Slurm(
        job_name="cleanProcessors",
        account="def-jphickey",
        time="00:01:00",
        nodes=1,
        ntasks_per_node=1,
        cpus_per_task={processors_per_job},
        mem_per_cpu="1G",
        output="OpenPFO.log",
        open_mode="append",
    )
    slurm1.set_wait(True)

    command = f"parallel rm -rf {case_directory}/processor{{}} ::: $(seq 0 {processors_per_job - 1})"
    slurm1.add_cmd(command)

    slurm1.sbatch()
    logger.info("Successfully ran cleanupProcessors.")

    # ==========================================================================

    slurm2 = Slurm(
        job_name="cleanCase",
        account="def-jphickey",
        time="00:01:00",
        nodes=1,
        ntasks_per_node=1,
        cpus_per_task=1,
        mem_per_cpu="100M",
        output="OpenPFO.log",
        open_mode="append",
    )
    slurm2.set_wait(True)

    slurm2.add_cmd(f"pyFoamClearCase.py {case_directory} --keep-postprocessing")
    slurm2.add_cmd(f"rm -rf {case_directory}/constant/polyMesh")

    slurm2.sbatch()
    logger.info("Successfully ran cleancCase")

    EXECUTE_CLEANUP_RETURN = ExecuteCleanupReturn()

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return EXECUTE_CLEANUP_RETURN
