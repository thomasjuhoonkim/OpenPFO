# fluidfoam
import fluidfoam

# classes
from classes.functions import ObjectivesParameters, ObjectivesReturn
from classes.objective import Objective

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
    meta = objectives_parameters.meta

    """ ======================= YOUR CODE BELOW HERE ======================= """

    force = fluidfoam.readforce(
        path=job_directory,
        namepatch="exitTotalPressureAvg",
        time_name="0",
        name="surfaceFieldValue",
    )

    P_o = force[-1][1]  # latest time & second index

    freestream_mach_value = meta.get_meta("freestream_mach")
    pressure_recovery_value = P_o / (
        26500 * (1 + (0.2 * (freestream_mach_value**2)) ** 3.5)
    )
    pressure_recovery = get_objective_by_id(objectives=objectives, id="pr")
    pressure_recovery.set_value(pressure_recovery_value)

    # ==========================================================================

    SHARED = "pvbatch --force-offscreen-rendering --opengl-window-backend OSMesa"
    FOAM_FILEPATH = f"{job_directory}/{job_id}.foam"
    COMMANDS = [
        f"{SHARED} input/paraview/mesh.py {FOAM_FILEPATH} {job_directory}",
        f"{SHARED} input/paraview/slice-velocity.py {FOAM_FILEPATH} {job_directory}",
        f"{SHARED} input/paraview/slice-pressure.py {FOAM_FILEPATH} {job_directory}",
        f"{SHARED} input/paraview/slice-mach.py {FOAM_FILEPATH} {job_directory}",
    ]

    slurm1 = Slurm(
        job_name=f"{job_id}-paraview",
        account="def-jphickey",
        time="00:10:00",
        nodes=1,
        ntasks_per_node=1,
        cpus_per_task=8,
        mem="8G",
        output=f"{job_directory}/paraview.log",
        open_mode="append",
    )
    slurm1.set_wait(True)

    for command in COMMANDS:
        slurm1.add_cmd(command)

    slurm1.sbatch()

    # slice
    meta.add_meta("pv-slice", "slice.png")

    # geometry
    meta.add_meta("pv-geometry-diagonal", "geometry-diagonal.png")
    meta.add_meta("pv-geometry-side", "geometry-side.png")

    # mesh
    meta.add_meta("pv-mesh", "mesh.png")

    # slice-velocity
    meta.add_meta("pv-slice-velocity", "slice-velocity.png")

    # slice-pressure
    meta.add_meta("pv-slice-pressure", "slice-pressure.png")

    # slice-mach
    meta.add_meta("pv-slice-mach", "slice-mach.png")

    OBJECTIVES_RETURN = ObjectivesReturn(objectives=objectives)

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return OBJECTIVES_RETURN
