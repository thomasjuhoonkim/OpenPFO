# classes
from classes.functions import CreateMeshParameters

# simple-slurm
from simple_slurm import Slurm


def create_mesh(
    create_mesh_parameters: CreateMeshParameters,
):
    """
    The create_mesh function is used to create the geometry for each grid
    point in the design space.

    NOTE: This function does not return a value.
    """

    """ ======================= YOUR CODE BELOW HERE ======================= """

    case_directory = create_mesh_parameters.output_case_directory
    logger = create_mesh_parameters.logger
    processors = create_mesh_parameters.processors

    slurm = Slurm(
        job_name="cartesianMesh",
        account="def-jphickey",
        time="00:05:00",
        nodes=1,
        ntasks_per_node=1,
        cpus_per_task=processors,
        mem="32G",
        output="OpenPFO.log",
        open_mode="append",
    )
    slurm.set_wait(True)

    slurm.add_cmd(
        f"surfaceTransformPoints -case {case_directory} -rotate-angle '((0 1 0) 5)' {case_directory}/original.stl {case_directory}/aoa.stl"
    )
    slurm.add_cmd(
        f"surfaceGenerateBoundingBox -case {case_directory} {case_directory}/aoa.stl {case_directory}/combined.stl 50 50 25 25 10 10"
    )
    slurm.add_cmd(
        f"surfaceFeatureEdges {case_directory}/combined.stl {case_directory}/combined.fms -angle 5 -case {case_directory}"
    )
    slurm.add_cmd(f"cartesianMesh -case {case_directory}")

    slurm_job_id = slurm.sbatch()
    logger.info(f"Successfully ran job {slurm_job_id} for cartesianMesh.")

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return None
