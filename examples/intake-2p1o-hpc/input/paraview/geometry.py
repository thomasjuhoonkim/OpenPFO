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

    VIEW_SIZE = [2021, 594]  

    renderView = CreateView("RenderView")
    renderView.ViewSize = VIEW_SIZE

    reader.MeshRegions = ["patch/internalMesh"]

    display = Show(reader, renderView)

    ColorBy(display, ("CELLS", ""))

    # Angle 1 - Diagonal
    renderView.CameraPosition = (12, 3.75, 16.5)
    renderView.CameraFocalPoint = [-7.9, 1, -3.9]  
    renderView.CameraViewUp = [0, 1, 0]  
    Render()
    SaveScreenshot(
        f"{job_directory}/geometry-diagonal.png",
        renderView,
        ImageResolution=renderView.ViewSize,
    )

    # Angle 2 - Side
    renderView.CameraPosition = [-12, 1.35, 23.5]
    renderView.CameraFocalPoint = [-12, 1.35, 0.0]
    renderView.CameraViewUp = [0, 1, 0]
    Render()
    SaveScreenshot(
        f"{job_directory}/geometry-side.png",
        renderView,
        ImageResolution=renderView.ViewSize,
    )

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    ResetSession()
