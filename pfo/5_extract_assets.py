# classes
from classes.functions import ExtractAssetsParameters

# simple-slurm
from simple_slurm import Slurm


def extract_assets(
    extract_assets_parameters: ExtractAssetsParameters,
):
    """
    The extract_assets function is used to add side effects to your optimization
    workflow such as image extractation and data analysis. The extract_assets
    function runs AFTER execute_solver and extract_objectives.

    All data from this function will be available to export after the full
    workflow has completed. You may store any data from this function in the
    provided assets output directory.

    NOTE: This function does not return a value.
    """

    """ ======================= YOUR CODE BELOW HERE ======================= """

    case_directory = extract_assets_parameters.output_case_foam_filepath
    output_directory = extract_assets_parameters.output_assets_directory
    logger = extract_assets_parameters.logger

    commands = [
        f"pvbatch input/paraview/slice.py {case_directory} {output_directory}",
        f"pvbatch input/paraview/geometry.py {case_directory} {output_directory}",
        f"pvbatch input/paraview/mesh.py {case_directory} {output_directory}",
        f"pvbatch input/paraview/streamline.py {case_directory} {output_directory}",
        f"pvbatch input/paraview/streamline-half.py {case_directory} {output_directory}",
        f"pvbatch input/paraview/slice-velocity.py {case_directory} {output_directory}",
        f"pvbatch input/paraview/slice-pressure.py {case_directory} {output_directory}",
    ]

    slurm = Slurm(
        job_name="extractAssets",
        account="def-jphickey",
        time="00:05:00",
        nodes=1,
        ntasks_per_node=1,
        cpus_per_task=1,
        mem_per_cpu="1G",
        array=range(len(commands)),
        output="OpenPFO.log",
        open_mode="append",
    )
    slurm.set_wait(True)

    for command in commands:
        slurm.add_cmd(command)

    slurm_job_id = slurm.sbatch()
    logger.info(f"Successfully ran job {slurm_job_id} for extractAssets.")

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return None
