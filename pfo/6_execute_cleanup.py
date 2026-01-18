# classes
from classes.functions import ExecuteCleanupParameters

# simple-slurm
from simple_slurm import Slurm


def execute_cleanup(
    execute_cleanup_parameters: ExecuteCleanupParameters,
):
    """
    The execute_cleanup function used to clean up solver artifacts after each job.

    NOTE: This function does not return a value.
    """

    """ ======================= YOUR CODE BELOW HERE ======================= """

    case_directory = execute_cleanup_parameters.output_case_directory
    logger = execute_cleanup_parameters.logger
    processors = execute_cleanup_parameters.processors

    slurm1 = Slurm(
        job_name="cleanupProcessors",
        account="def-jphickey",
        time="00:05:00",
        nodes=1,
        ntasks_per_node=1,
        cpus_per_task={processors},
        mem_per_cpu="1G",
        output="OpenPFO.log",
        open_mode="append",
    )
    slurm1.set_wait(True)

    command = (
        f"parallel rm -rf {case_directory}/processor{{}} ::: $(seq 0 {processors - 1})"
    )
    slurm1.add_cmd(command)

    slurm_job_id = slurm1.sbatch()
    logger.info(f"Successfully ran job {slurm_job_id} for cleanup processors.")

    # ==========================================================================

    slurm2 = Slurm(
        job_name="foamCleanCase",
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

    slurm2.add_cmd("foamCleanCase")

    slurm_job_id = slurm2.sbatch()
    logger.info(f"Successfully ran job {slurm_job_id} for foamCleanCase.")

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return None
