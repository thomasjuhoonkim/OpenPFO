# system
import os

# classes
from classes.functions import CreateMeshParameters, CreateMeshReturn

# simple-slurm
from simple_slurm import Slurm


def create_mesh(
    create_mesh_parameters: CreateMeshParameters,
):
    """
    The create_mesh function is used to create the geometry for each grid
    point in the design space.
    """

    """ ======================= YOUR CODE BELOW HERE ======================= """

    case_directory = create_mesh_parameters.output_case_directory
    logger = create_mesh_parameters.logger
    processors_per_job = create_mesh_parameters.processors_per_job
    job_id = create_mesh_parameters.job_id

    slurm = Slurm(
        job_name=f"{job_id}-cartesianMesh",
        account="def-jphickey",
        time="00:10:00",
        nodes=1,
        ntasks_per_node=1,
        cpus_per_task=processors_per_job,
        mem="48G",
        output=f"{case_directory}/cartesianMesh.log",
        open_mode="append",
    )
    slurm.set_wait(True)

    slurm.add_cmd(
        f"surfaceGenerateBoundingBox -case {case_directory} {case_directory}/original.stl {case_directory}/combined.stl 50 50 25 25 10 10"
    )
    slurm.add_cmd(
        f"surfaceFeatureEdges {case_directory}/combined.stl {case_directory}/combined.fms -angle 5 -case {case_directory}"
    )
    slurm.add_cmd(f"cartesianMesh -case {case_directory}")

    slurm.sbatch()
    logger.info("Successfully ran cartesianMesh.")

    # VALIDATION ===============================================================

    run_ok = True
    if not os.path.isdir(f"{case_directory}/constant/polyMesh"):
        run_ok = False

    CREATE_MESH_RETURN = CreateMeshReturn(run_ok=run_ok)

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return CREATE_MESH_RETURN
