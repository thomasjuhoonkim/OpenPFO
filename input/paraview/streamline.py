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
    reader1 = OpenDataFile(input_filepath)
    reader2 = OpenDataFile(input_filepath)

    """ ======================= YOUR CODE BELOW HERE ======================= """

    VIEW_SIZE = [3840, 2160]

    renderView = CreateView("RenderView")
    renderView.ViewSize = VIEW_SIZE

    renderView.CameraPosition = [-1.25, 1.25, 1]
    renderView.CameraFocalPoint = [0.5, 0, 0]
    renderView.CameraViewUp = [0, 0, 1]

    renderView.OrientationAxesVisibility = 0

    display1 = Show(reader1, renderView)
    ColorBy(display1, ("CELLS", ""))

    reader2.MeshRegions = ["patch/solid"]
    display2 = Show(reader2, renderView)
    ColorBy(display2, ("CELLS", ""))

    streamTracer = StreamTracer(Input=reader1, SeedType="Line")
    streamTracer.SeedType.Point1 = [-10, -0.5, 0]
    streamTracer.SeedType.Point2 = [-10, 0.5, 0]
    streamTracer.SeedType.Resolution = 100
    streamTracer.Vectors = ["POINTS", "U"]

    streamTracerDisplay = Show(streamTracer, renderView)

    tube = Tube(Input=streamTracer)
    tube.Radius = 0.0025

    tubeDisplay = Show(tube, renderView)
    tubeDisplay.SetScalarBarVisibility(renderView, True)
    tubeDisplay.RescaleTransferFunctionToDataRange(True, False)

    ColorBy(tubeDisplay, ("POINTS", "U", "Magnitude"))
    uLUT = GetColorTransferFunction("U")
    HideScalarBarIfNotNeeded(uLUT, renderView)
    tubeDisplay.RescaleTransferFunctionToDataRange(True, False)
    tubeDisplay.SetScalarBarVisibility(renderView, True)

    Hide(reader1, renderView)
    Hide(streamTracer, renderView)

    Render()

    SaveScreenshot(
        f"{job_directory}/streamline.png",
        renderView,
        ImageResolution=renderView.ViewSize,
    )

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    ResetSession()
