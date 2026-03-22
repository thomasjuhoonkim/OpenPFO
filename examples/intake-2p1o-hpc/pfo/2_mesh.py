# system
import os

# classes
from classes.functions import MeshParameters, MeshReturn

# simple-slurm
from simple_slurm import Slurm


def mesh(
    mesh_parameters: MeshParameters,
):
    """
    The function is used to generate a mesh for each point in the design space.
    """

    job_directory = mesh_parameters.job_directory
    processors_per_job = mesh_parameters.processors_per_job
    logger = mesh_parameters.logger
    job_id = mesh_parameters.job_id
    point = mesh_parameters.point
    meta = mesh_parameters.meta

    """ ======================= YOUR CODE BELOW HERE ======================= """
    # pinitial conditions fie modifications
    
    free_stream_mach = 5.5 #FROM CADQUERY
    a = 300 #SPEED OF SOUND AT 10KM
    inlet_speed = ( free_stream_mach * a )
    

    # case
    initialConditions_filepath = f"{job_directory}/0/include/initialConditions"
    initialConditions_file = ParsedParameterFile(initialConditions_filepath)

    # modify values
    initialConditions_file["velocityInlet"] = a
    v_vector = f"({inlet_speed} 0 0)"
    initialConditions_file["velocityField"] = v_vector
    initialConditions_file["velocityOutlet"] = v_vector

    ground_height_variable = point.get_variables()[-1]
    ground_height = ground_height_variable.get_value()

    COMMANDS = [
        f"blockMesh -case {job_directory}",
    ]

    slurm = Slurm(
        job_name=f"{job_id}-blockMesh",
        account="def-jphickey",
        time="00:10:00",
        nodes=1,
        ntasks_per_node=1,
        cpus_per_task=processors_per_job,
        mem="32G",
        output=f"{job_directory}/blockMesh.log",
        open_mode="append",
    )
    slurm.set_wait(True)

    for command in COMMANDS:
        slurm.add_cmd(command)

    slurm.sbatch()

    # VALIDATION ===============================================================

    run_ok = True
    if not os.path.isdir(f"{job_directory}/constant/polyMesh"):
        run_ok = False

    MESH_RETURN = MeshReturn(run_ok=run_ok)

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return MESH_RETURN
