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
        cpus_per_task=1,
        mem_per_cpu="100M",
        array=range(processors),
        output="OpenPFO.log",
        open_mode="append",
    )
    slurm1.set_wait(True)

    slurm1.add_cmd(
        f"""
DIR_TO_DELETE="{case_directory}/processor${{SLURM_ARRAY_TASK_ID}}"

# Check if the directory exists and delete it
if [ -d "$DIR_TO_DELETE" ]; then
    echo "Task $SLURM_ARRAY_TASK_ID: Deleting directory $DIR_TO_DELETE"
    rm -rf "$DIR_TO_DELETE"
else
    echo "Task $SLURM_ARRAY_TASK_ID: Directory $DIR_TO_DELETE not found, skipping"
fi
"""
    )

    slurm_job_id = slurm1.sbatch()
    logger.info(f"Successfully ran job {slurm_job_id} for cleanup processors.")

    # ==========================================================================

    slurm2 = Slurm(
        job_name="foamCleanCase",
        account="def-jphickey",
        time="00:05:00",
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
