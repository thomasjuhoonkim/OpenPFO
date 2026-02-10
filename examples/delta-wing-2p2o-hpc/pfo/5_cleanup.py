# system
import subprocess

# classes
from classes.functions import CleanupParameters, CleanupReturn

# simple-slurm
from simple_slurm import Slurm


def cleanup(
    cleanup_parameters: CleanupParameters,
):
    """
    This function is used to clean up artifacts after each job.
    """
    job_directory = cleanup_parameters.job_directory
    processors_per_job = cleanup_parameters.processors_per_job
    logger = cleanup_parameters.logger
    job_id = cleanup_parameters.job_id
    point = cleanup_parameters.point
    meta = cleanup_parameters.meta

    """ ======================= YOUR CODE BELOW HERE ======================= """

    # slurm = Slurm(
    #     job_name=f"{job_id}-cleanProcessors",
    #     account="def-jphickey",
    #     time="00:01:00",
    #     nodes=1,
    #     ntasks_per_node=1,
    #     cpus_per_task={processors_per_job},
    #     mem_per_cpu="1G",
    #     output=f"{job_directory}/OpenPFO.log",
    #     open_mode="append",
    # )
    # slurm.set_wait(True)

    # command = f"parallel rm -rf {job_directory}/processor{{}} ::: $(seq 0 {processors_per_job - 1})"
    # slurm.add_cmd(command)

    # slurm.sbatch()

    # ==========================================================================

    COMMANDS = (
        f"pyFoamClearCase.py {job_directory} --keep-postprocessing --processors-remove",
        f"rm -rf {job_directory}/constant/polyMesh",
    )

    for command in COMMANDS:
        subprocess.run(command.split(" "), capture_output=True, text=True, check=True)

    CLEANUP_RETURN = CleanupReturn()

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return CLEANUP_RETURN
