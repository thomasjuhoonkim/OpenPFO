# fluidfoam
import fluidfoam

# classes
from classes.functions import ObjectivesParameters, ObjectivesReturn
from classes.objective import Objective

# util
from util.run_parallel_commands import run_parallel_commands

# simple-slurm
from simple_slurm import Slurm


def objectives(
    objectives_parameters: ObjectivesParameters,
) -> ObjectivesReturn:
    """
    This function is used to extract objectives and export data for each job.

    NOTE: This function MUST modify the original list of objectives and return it.
    """

    def get_objective_by_id(objectives: list[Objective], id: str):
        return next((o for o in objectives if o.get_id() == id), None)

    job_directory = objectives_parameters.job_directory
    processors_per_job = objectives_parameters.processors_per_job
    objectives = objectives_parameters.objectives
    job_id = objectives_parameters.job_id
    logger = objectives_parameters.logger
    point = objectives_parameters.point

    """ ======================= YOUR CODE BELOW HERE ======================= """

    force = fluidfoam.readforce(
        path=job_directory,
        namepatch="forceCoeffs1",
        time_name="0",
        name="coefficient",
    )

    c_d = get_objective_by_id(objectives=objectives, id="cd")
    c_d.set_value(force[-1][1])  # latest time & second index (Cd - maximize)

    c_l = get_objective_by_id(objectives=objectives, id="cl")
    c_l.set_value(force[-1][4])  # latest time & fourth index (Cl - minimize)

    # ==========================================================================

    # SHARED = "/Applications/ParaView-6.0.1.app/Contents/bin/pvbatch"
    SHARED = "pvbatch --force-offscreen-rendering --opengl-window-backend OSMesa"
    FOAM_FILEPATH = f"{job_directory}/{job_id}.foam"
    COMMANDS = [
        f"{SHARED} input/paraview/slice.py {FOAM_FILEPATH} {job_directory}",
        f"{SHARED} input/paraview/geometry.py {FOAM_FILEPATH} {job_directory}",
        f"{SHARED} input/paraview/mesh.py {FOAM_FILEPATH} {job_directory}",
        f"{SHARED} input/paraview/streamline.py {FOAM_FILEPATH} {job_directory}",
        f"{SHARED} input/paraview/streamline-half.py {FOAM_FILEPATH} {job_directory}",
        f"{SHARED} input/paraview/slice-velocity.py {FOAM_FILEPATH} {job_directory}",
        f"{SHARED} input/paraview/slice-pressure.py {FOAM_FILEPATH} {job_directory}",
        f"{SHARED} input/paraview/yplus.py {FOAM_FILEPATH} {job_directory}",
        f"{SHARED} input/paraview/cp-contour.py {FOAM_FILEPATH} {job_directory}",
        f"{SHARED} input/paraview/wall-shear.py {FOAM_FILEPATH} {job_directory}",
    ]

    # run_parallel_commands(commands=COMMANDS, max_workers=processors_per_job)

    slurm1 = Slurm(
        job_name=f"{job_id}-paraview",
        account="def-jphickey",
        time="00:05:00",
        nodes=1,
        ntasks_per_node=1,
        cpus_per_task=16,
        mem_per_cpu="4G",
        output=f"{job_directory}/paraview.log",
        open_mode="append",
    )
    slurm1.set_wait(True)

    for command in COMMANDS:
        slurm1.add_cmd(command)

    slurm1.sbatch()

    # ==========================================================================

    # slurm2 = Slurm(
    #     job_name=f"{job_id}-foamToVTK",
    #     account="def-jphickey",
    #     time="00:05:00",
    #     nodes=1,
    #     ntasks_per_node=processors_per_job,
    #     mem_per_cpu="1G",
    #     output=f"{job_directory}/foamToVTK.log",
    #     open_mode="append",
    # )
    # slurm2.set_wait(True)

    # slurm2.add_cmd(
    #     f"mpirun -np {processors_per_job} foamToVTK -parallel -latestTime -case {job_directory}",
    # )
    # slurm2.add_cmd(
    #     f"mv {job_directory}/VTK {output_directory}",
    # )

    # slurm2.sbatch()

    OBJECTIVES_RETURN = ObjectivesReturn(objectives=objectives)

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return OBJECTIVES_RETURN
