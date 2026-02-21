# fluidfoam
import fluidfoam

# classes
from classes.functions import ObjectivesParameters, ObjectivesReturn
from classes.objective import Objective

# util
from util.run_parallel_commands import run_parallel_commands


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
        namepatch="forceCoeffs1",
        time_name="0",
        name="coefficient",
    )

    c_d = get_objective_by_id(objectives=objectives, id="cd")
    c_d.set_value(force[-1][1])  # latest time & second index (Cd - maximize)

    c_l = get_objective_by_id(objectives=objectives, id="cl")
    c_l.set_value(force[-1][4])  # latest time & fourth index (Cl - minimize)

    volume_value = meta.get_meta("volume")
    volume = get_objective_by_id(objectives=objectives, id="volume")
    volume.set_value(volume_value)

    # ==========================================================================

    SHARED = "/Applications/ParaView-6.0.1.app/Contents/bin/pvbatch"
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

    run_parallel_commands(commands=COMMANDS, max_workers=processors_per_job)

    # slice
    meta.add_meta("pv-slice", "slice.png")

    # geometry
    meta.add_meta("pv-geometry-diagonal", "geometry-diagonal.png")
    meta.add_meta("pv-geometry-front", "geometry-front.png")
    meta.add_meta("pv-geometry-side", "geometry-side.png")
    meta.add_meta("pv-geometry-top", "geometry-top.png")
    meta.add_meta("pv-geometry-bottom", "geometry-bottom.png")

    # mesh
    meta.add_meta("pv-mesh", "mesh.png")

    # streamline
    meta.add_meta("pv-streamline-diagonal", "streamline-diagonal.png")
    meta.add_meta("pv-streamline-front", "streamline-front.png")
    meta.add_meta("pv-streamline-side", "streamline-side.png")
    meta.add_meta("pv-streamline-top", "streamline-top.png")
    meta.add_meta("pv-streamline-bottom", "streamline-bottom.png")

    # streamline-half
    meta.add_meta("pv-streamline-half", "streamline-half.png")

    # slice-velocity
    meta.add_meta("pv-slice-velocity", "slice-velocity.png")

    # slice-pressure
    meta.add_meta("pv-slice-pressure", "slice-pressure.png")

    # yplus
    meta.add_meta("pv-yplus-diagonal", "yplus-diagonal.png")
    meta.add_meta("pv-yplus-front", "yplus-front.png")
    meta.add_meta("pv-yplus-side", "yplus-side.png")
    meta.add_meta("pv-yplus-top", "yplus-top.png")
    meta.add_meta("pv-yplus-bottom", "yplus-bottom.png")

    # cp-contour
    meta.add_meta("pv-cp-contour-diagonal", "cp-contour-diagonal.png")
    meta.add_meta("pv-cp-contour-front", "cp-contour-front.png")
    meta.add_meta("pv-cp-contour-side", "cp-contour-side.png")
    meta.add_meta("pv-cp-contour-top", "cp-contour-top.png")
    meta.add_meta("pv-cp-contour-bottom", "cp-contour-bottom.png")

    # wall-shear
    meta.add_meta("pv-wall-shear-diagonal", "wall-shear-diagonal.png")
    meta.add_meta("pv-wall-shear-front", "wall-shear-front.png")
    meta.add_meta("pv-wall-shear-side", "wall-shear-side.png")
    meta.add_meta("pv-wall-shear-top", "wall-shear-top.png")
    meta.add_meta("pv-wall-shear-bottom", "wall-shear-bottom.png")

    OBJECTIVES_RETURN = ObjectivesReturn(objectives=objectives)

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return OBJECTIVES_RETURN
