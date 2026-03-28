# classes
from classes.functions import GeometryParameters, GeometryReturn

import numpy as np
from scipy.integrate import solve_ivp

# PyFoam
from PyFoam.RunDictionary.ParsedBlockMeshDict import ParsedBlockMeshDict
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile


def geometry(
    geometry_parameters: GeometryParameters,
) -> GeometryReturn:
    """
    This function is used to generate the geometry for each point in the design space.
    """

    job_directory = geometry_parameters.job_directory
    processors_per_job = geometry_parameters.processors_per_job
    job_id = geometry_parameters.job_id
    logger = geometry_parameters.logger
    point = geometry_parameters.point
    meta = geometry_parameters.meta

    """ ======================= YOUR CODE BELOW HERE ======================= """

    theta23 = np.deg2rad(69)
    M2 = 2.5

    variables = point.get_variables()
    for variable in variables:
        if variable.get_id() == "theta23_deg":
            theta23 = np.deg2rad(variable.get_value())
        if variable.get_id() == "M2":
            M2 = variable.get_value()

    def TM(theta, y):
        u, v, r = y
        A = (u + v / np.tan(theta)) / (v * v - 1)
        du = v + (gamma - 1) / 2 * u * v * (A)
        dv = -u + (1 + (gamma - 1) / 2 * v * v) * (A)
        dr = r * u / v
        return [du, dv, dr]

    gamma = 1.4

    def pol2cart(rho, phi):
        x = rho * np.cos(phi)
        y = rho * np.sin(phi)
        return (x, y)

    def theta_beta_m(M, beta):
        return np.arctan(
            2
            / np.tan(beta)
            * (
                (M**2 * np.sin(beta) ** 2 - 1)
                / (2 * M * M * (gamma + 1 - (2 * np.sin(beta) ** 2)))
            )
        )

    # inlet height
    offset_y = 0.0
    # thickness
    offset_z = 0.1

    u2 = M2 * np.cos(theta23)
    v2 = -M2 * np.sin(theta23)

    delta23 = theta_beta_m(M2, theta23)

    theta2 = theta23 - delta23

    sol = solve_ivp(TM, (theta2, np.pi), [u2, v2, 1], max_step=0.01)

    M = np.sqrt(sol.y[0] ** 2 + sol.y[1] ** 2)
    idx = np.argmax(M)
    x, y = pol2cart(sol.y[2][:idx], sol.t[:idx])

    # normalize X to start at 0
    x_offset = x[0]

    # generate points in 3D
    points_left = []
    points_right = []

    for xi, yi in zip(x, y):
        px = float(xi - x_offset)
        py = float(yi + offset_y)
        points_left.append((px, py, offset_z))
        points_right.append((px, py, -offset_z))

    with open(f"{job_directory}/left_spline.csv", "w") as f:
        for p in points_left:
            f.write(f"{p[0]},{p[1]},{p[2]}\n")

    with open(f"{job_directory}/right_spline.csv", "w") as f:
        for p in points_right:
            f.write(f"{p[0]},{p[1]},{p[2]}\n")

    # ==========================================================================

    block_mesh_dict_filepath = f"{job_directory}/system/blockMeshDict"
    block_mesh_dict_file = ParsedBlockMeshDict(block_mesh_dict_filepath)

    inlet_x = points_left[-1][0]
    inlet_y = points_left[-1][1]
    outlet_x = points_left[0][0]
    outlet_y = points_left[0][1]

    divisionsX = int(np.ceil(38.2 * (outlet_x - inlet_x)))
    divisionsY = int(np.ceil(33.36 * inlet_y))

    block_mesh_dict_file["inletX2"] = inlet_x - 10
    block_mesh_dict_file["inletX"] = inlet_x
    block_mesh_dict_file["inletY"] = inlet_y
    block_mesh_dict_file["outletX"] = outlet_x
    block_mesh_dict_file["outletY"] = outlet_y
    block_mesh_dict_file["div_x"] = divisionsX
    block_mesh_dict_file["div_y"] = divisionsY
    block_mesh_dict_file["edges"][3] = [
        [px, py, "$inletZ"] for px, py, _ in points_left
    ]
    block_mesh_dict_file["edges"][7] = [
        [px, py, "$inletZ_neg"] for px, py, _ in points_right
    ]
    block_mesh_dict_file.writeFile()

    freestream_mach = M[idx]
    a = 300  # speed of sound at 10km
    inlet_speed = freestream_mach * a

    # case
    initialConditions_filepath = f"{job_directory}/0/include/initialConditions"
    initialConditions_file = ParsedParameterFile(initialConditions_filepath)

    # modify values
    initialConditions_file["velocityInlet"] = inlet_speed
    v_vector = f"({inlet_speed} 0 0)"
    initialConditions_file["velocityField"] = v_vector
    initialConditions_file["velocityOutlet"] = v_vector

    initialConditions_file.writeFile()

    GEOMETRY_RETURN = GeometryReturn(visualize_filepath="")

    meta.add_meta("freestream_mach", freestream_mach)

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return GEOMETRY_RETURN
