# classes
from classes.functions import ExtractAssetsParameters, ExtractAssetsReturn

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
    """

    """ ======================= YOUR CODE BELOW HERE ======================= """

    case_foam_filepath = extract_assets_parameters.output_case_foam_filepath
    # case_directory = extract_assets_parameters.output_case_directory
    output_directory = extract_assets_parameters.output_assets_directory
    # processors_per_job = extract_assets_parameters.processors_per_job
    logger = extract_assets_parameters.logger

    slurm1 = Slurm(
        job_name="paraview",
        account="def-jphickey",
        time="00:05:00",
        nodes=1,
        ntasks_per_node=1,
        cpus_per_task=16,
        mem_per_cpu="4G",
        output="OpenPFO.log",
        open_mode="append",
    )
    slurm1.set_wait(True)

    SHARED = "pvbatch --force-offscreen-rendering --opengl-window-backend OSMesa"
    commands = [
        f"{SHARED} input/paraview/slice.py {case_foam_filepath} {output_directory}",
        f"{SHARED} input/paraview/geometry.py {case_foam_filepath} {output_directory}",
        f"{SHARED} input/paraview/mesh.py {case_foam_filepath} {output_directory}",
        f"{SHARED} input/paraview/streamline.py {case_foam_filepath} {output_directory}",
        f"{SHARED} input/paraview/streamline-half.py {case_foam_filepath} {output_directory}",
        f"{SHARED} input/paraview/slice-velocity.py {case_foam_filepath} {output_directory}",
        f"{SHARED} input/paraview/slice-pressure.py {case_foam_filepath} {output_directory}",
    ]
    for command in commands:
        slurm1.add_cmd(command)

    slurm1.sbatch()
    logger.info("Successfully ran paraview.")

    # ==========================================================================

    # slurm2 = Slurm(
    #     job_name="foamToVTK",
    #     account="def-jphickey",
    #     time="00:05:00",
    #     nodes=1,
    #     ntasks_per_node=processors_per_job,
    #     mem_per_cpu="1G",
    #     output="OpenPFO.log",
    #     open_mode="append",
    # )
    # slurm2.set_wait(True)

    # slurm2.add_cmd(
    #     f"mpirun -np {processors_per_job} foamToVTK -parallel -latestTime -case {case_directory}",
    # )
    # slurm2.add_cmd(
    #     f"mv {case_directory}/VTK {output_directory}",
    # )

    # slurm2.sbatch()
    # logger.info("Successfully ran foamToVTK.")

    EXTRACT_ASSETS_RETURN = ExtractAssetsReturn()

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return EXTRACT_ASSETS_RETURN
