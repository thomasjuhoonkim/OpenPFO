import sys

from paraview.simple import *

paraview.simple._DisableFirstRenderCameraReset()

if __name__ == "__main__":
    # validate inputs
    if len(sys.argv) < 3:
        print("Usage: pvbatch -- pvbatch.py <input_filepath> <assets_directory>")
        sys.exit(1)

    # parse inputs
    input_filepath = sys.argv[1]
    assets_directory = sys.argv[2]

    # load data
    reader1 = OpenDataFile(input_filepath)
    reader2 = OpenDataFile(input_filepath)

    """ ======================= YOUR CODE BELOW HERE ======================= """

    VIEW_SIZE = [3840, 2160]

    renderView = CreateView("RenderView")
    renderView.ViewSize = VIEW_SIZE

    renderView.CameraPosition = [-0.5, 0.5, 0.25]
    renderView.CameraFocalPoint = [0.6, 0, 0]
    renderView.CameraViewUp = [0, 0, 1]

    renderView.OrientationAxesVisibility = 0

    slice = Slice(Input=reader1)
    slice.SliceType = "Plane"
    slice.SliceType.Origin = [0.5, 0, 0]
    slice.SliceType.Normal = [1, 0, 0]
    # slice.Crinkleslice = True

    display1 = Show(slice, renderView)
    display1.Representation = "Surface With Edges"
    ColorBy(display1, ("CELLS", ""))

    reader2.MeshRegions = ["patch/jobGeometry"]

    display2 = Show(reader2, renderView)
    display2.Representation = "Surface With Edges"
    ColorBy(display2, ("CELLS", ""))

    Render()

    SaveScreenshot(
        f"{assets_directory}/mesh.png",
        renderView,
        ImageResolution=renderView.ViewSize,
    )

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    ResetSession()
