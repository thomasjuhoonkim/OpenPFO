import os
import shutil

import pyvista as pv


def test():
    geometries = os.listdir("output/geometries")
    geometries.sort()
    os.mkdir("temp")

    for geometry in geometries:
        original = f"output/geometries/{geometry}"
        filename = geometry.split(".")
        dest = shutil.copy(original, f"temp/{filename[0]}.stl")
        print(dest)
        mesh = pv.read(dest)
        mesh.plot()
