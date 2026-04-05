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

    parafoam = GetActiveSource()
    parafoam.MeshRegions = ["patch/solid"]

    wallShearStressLUT = GetColorTransferFunction("wallShearStress")
    HideScalarBarIfNotNeeded(wallShearStressLUT, renderView)

    display1 = GetRepresentation(parafoam, renderView)
    # display1.Representation = "Surface With Edges"

    UpdateScalarBarsComponentTitle(wallShearStressLUT, display1)

    ColorBy(display1, ("CELLS", "wallShearStress", "X"))
    display1.RescaleTransferFunctionToDataRange(True, False)
    display1.SetScalarBarVisibility(renderView, True)

    # Angle 1 - Diagonal
    renderView.CameraPosition = [-1.25, 1.25, 1]
    renderView.CameraFocalPoint = [0.5, 0, 0]
    renderView.CameraViewUp = [0, 0, 1]
    Render()
    SaveScreenshot(
        f"{job_directory}/wall-shear-diagonal.png",
        renderView,
        ImageResolution=renderView.ViewSize,
    )

    # Angle 2 - Front
    renderView.CameraPosition = [-1.25, 0, 0]
    renderView.CameraFocalPoint = [0.5, 0, 0]
    renderView.CameraViewUp = [0, 0, 1]
    Render()
    SaveScreenshot(
        f"{job_directory}/wall-shear-front.png",
        renderView,
        ImageResolution=renderView.ViewSize,
    )

    # Angle 3 - Side
    renderView.CameraPosition = [0, 2.5, 0]
    renderView.CameraFocalPoint = [0.5, 0, 0]
    renderView.CameraViewUp = [0, 0, 1]
    Render()
    SaveScreenshot(
        f"{job_directory}/wall-shear-side.png",
        renderView,
        ImageResolution=renderView.ViewSize,
    )

    # Angle 4 - Top
    renderView.CameraPosition = [0, 0, 3]
    renderView.CameraFocalPoint = [0.5, 0, 0]
    renderView.CameraViewUp = [0, 0, 1]
    Render()
    SaveScreenshot(
        f"{job_directory}/wall-shear-top.png",
        renderView,
        ImageResolution=renderView.ViewSize,
    )

    # Angle 5 - Bottom
    renderView.CameraPosition = [0, 0, -3]
    renderView.CameraFocalPoint = [0.5, 0, 0]
    renderView.CameraViewUp = [0, 0, -1]
    Render()
    SaveScreenshot(
        f"{job_directory}/wall-shear-bottom.png",
        renderView,
        ImageResolution=renderView.ViewSize,
    )

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    ResetSession()
