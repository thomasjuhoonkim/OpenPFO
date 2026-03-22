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

    VIEW_SIZE = [2021, 594]  

    renderView = CreateView("RenderView")
    renderView.ViewSize = VIEW_SIZE

    renderView.CameraPosition = [-12, 1.35, 23.5]
    renderView.CameraFocalPoint = [-12, 1.35, 0.0]
    renderView.CameraViewUp = [0, 1, 0]

    slice = Slice(Input=reader)
    slice.SliceType = "Plane"
    slice.SliceType.Origin = [0, 0, 0] 
    slice.SliceType.Normal = [0, 0, 1]             

    uLUT = GetColorTransferFunction("U")
    HideScalarBarIfNotNeeded(uLUT, renderView)

    display1 = Show(slice, renderView)

    ColorBy(display1, ("CELLS", "U", "Magnitude"))
    display1.RescaleTransferFunctionToDataRange(True, False)
    display1.SetScalarBarVisibility(renderView, True)

    Render()

    SaveScreenshot(
        f"{job_directory}/slice-velocity.png",
        renderView,
        ImageResolution=renderView.ViewSize,
    )

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    ResetSession()
