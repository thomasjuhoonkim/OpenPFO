import sys

from paraview.simple import *

paraview.simple._DisableFirstRenderCameraReset()

if __name__ == "__main__":
    # validate inputs
    if len(sys.argv) < 3:
        print("Usage: pvbatch -- script.py <input_filepath> <job_directory>")
        sys.exit(1)

    # parse inputs
    input_filepath = sys.argv[1]
    job_directory = sys.argv[2]

    # load data
    reader = OpenDataFile(input_filepath)

    """ ======================= YOUR CODE BELOW HERE ======================= """

    VIEW_SIZE = [3840, 2160]

    renderView = CreateView("RenderView")
    renderView.ViewSize = VIEW_SIZE

    renderView.CameraPosition = [-1.25, 1.25, 1]
    renderView.CameraFocalPoint = [0.5, 0, 0]
    renderView.CameraViewUp = [0, 0, 1]

    parafoam = GetActiveSource()
    parafoam.MeshRegions = ["patch/solid"]

    wallShearStressLUT = GetColorTransferFunction("wallShearStress")
    HideScalarBarIfNotNeeded(wallShearStressLUT, renderView)

    display1 = GetRepresentation(parafoam, renderView)
    display1.RescaleTransferFunctionToDataRange(True, False)
    display1.SetScalarBarVisibility(renderView, True)
    # display1.Representation = "Surface With Edges"

    UpdateScalarBarsComponentTitle(wallShearStressLUT, display1)

    ColorBy(display1, ("CELLS", "wallShearStress", "X"))

    Render()

    SaveScreenshot(
        f"{job_directory}/wall-shear.png",
        renderView,
        ImageResolution=renderView.ViewSize,
    )

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    ResetSession()
