import sys

from paraview.simple import *

paraview.simple._DisableFirstRenderCameraReset()

if __name__ == "__main__":
    # validate inputs
    if len(sys.argv) < 3:
        print("Usage: pvbatch -- pvbatch.py <input_filepath> <job_directory>")
        sys.exit(1)

    # parse inputs
    input_filepath = sys.argv[1]
    job_directory = sys.argv[2]

    # load data
    reader = OpenDataFile(input_filepath)

    """ ======================= YOUR CODE BELOW HERE ======================= """

    VIEW_SIZE = [15360, 8640]

    renderView = CreateView("RenderView")
    renderView.ViewSize = VIEW_SIZE

    reader.MeshRegions = ["patch/solid"]

    display = Show(reader, renderView)

    ColorBy(display, ("CELLS", ""))

    # Angle 1 - Diagonal
    renderView.CameraPosition = [-1, 1, 1]
    renderView.CameraFocalPoint = [0.6, 0, 0]
    renderView.CameraViewUp = [0, 0, 1]
    Render()
    SaveScreenshot(
        f"{job_directory}/geometry-diagonal.png",
        renderView,
        ImageResolution=renderView.ViewSize,
    )

    # Angle 2 - Front
    renderView.CameraPosition = [-1, 0, 0]
    renderView.CameraFocalPoint = [0.6, 0, 0]
    renderView.CameraViewUp = [0, 0, 1]
    Render()
    SaveScreenshot(
        f"{job_directory}/geometry-front.png",
        renderView,
        ImageResolution=renderView.ViewSize,
    )

    # Angle 3 - Side
    renderView.CameraPosition = [0, 2, 0]
    renderView.CameraFocalPoint = [0.6, 0, 0]
    renderView.CameraViewUp = [0, 0, 1]
    Render()
    SaveScreenshot(
        f"{job_directory}/geometry-side.png",
        renderView,
        ImageResolution=renderView.ViewSize,
    )

    # Angle 4 - Top
    renderView.CameraPosition = [0, 0, 3]
    renderView.CameraFocalPoint = [0.6, 0, 0]
    renderView.CameraViewUp = [0, 0, 1]
    Render()
    SaveScreenshot(
        f"{job_directory}/geometry-top.png",
        renderView,
        ImageResolution=renderView.ViewSize,
    )

    # Angle 5 - Bottom
    renderView.CameraPosition = [0, 0, -3]
    renderView.CameraFocalPoint = [0.6, 0, 0]
    renderView.CameraViewUp = [0, 0, -1]
    Render()
    SaveScreenshot(
        f"{job_directory}/geometry-bottom.png",
        renderView,
        ImageResolution=renderView.ViewSize,
    )

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    ResetSession()
