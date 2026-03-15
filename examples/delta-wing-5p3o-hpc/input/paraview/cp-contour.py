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

    pLUT = GetColorTransferFunction("p")
    HideScalarBarIfNotNeeded(pLUT, renderView)

    calculator1 = Calculator(registrationName="Calculator1", Input=parafoam)

    calculator1.Set(
        ResultArrayName="Cp",
        Function="(p - 0)/(0.5*1.225*(10^2))",
    )
    calculator1.AttributeType = "Cell Data"

    cpLUT = GetColorTransferFunction("Cp")
    cpPWF = GetOpacityTransferFunction("Cp")
    cpTF2D = GetTransferFunction2D("Cp")

    display1 = Show(calculator1, renderView)
    display1.RescaleTransferFunctionToDataRange(True, False)
    display1.SetScalarBarVisibility(renderView, True)

    ColorBy(display1, ("CELLS", "Cp"))
    Hide(parafoam, renderView)

    # Angle 1 - Diagonal
    renderView.CameraPosition = [-1.25, 1.25, 1]
    renderView.CameraFocalPoint = [0.5, 0, 0]
    renderView.CameraViewUp = [0, 0, 1]
    Render()
    SaveScreenshot(
        f"{job_directory}/cp-contour-diagonal.png",
        renderView,
        ImageResolution=renderView.ViewSize,
    )

    # Angle 2 - Front
    renderView.CameraPosition = [-1.25, 0, 0]
    renderView.CameraFocalPoint = [0.5, 0, 0]
    renderView.CameraViewUp = [0, 0, 1]
    Render()
    SaveScreenshot(
        f"{job_directory}/cp-contour-front.png",
        renderView,
        ImageResolution=renderView.ViewSize,
    )

    # Angle 3 - Side
    renderView.CameraPosition = [0, 2.5, 0]
    renderView.CameraFocalPoint = [0.5, 0, 0]
    renderView.CameraViewUp = [0, 0, 1]
    Render()
    SaveScreenshot(
        f"{job_directory}/cp-contour-side.png",
        renderView,
        ImageResolution=renderView.ViewSize,
    )

    # Angle 4 - Top
    renderView.CameraPosition = [0, 0, 3]
    renderView.CameraFocalPoint = [0.5, 0, 0]
    renderView.CameraViewUp = [0, 0, 1]
    Render()
    SaveScreenshot(
        f"{job_directory}/cp-contour-top.png",
        renderView,
        ImageResolution=renderView.ViewSize,
    )

    # Angle 5 - Bottom
    renderView.CameraPosition = [0, 0, -3]
    renderView.CameraFocalPoint = [0.5, 0, 0]
    renderView.CameraViewUp = [0, 0, -1]
    Render()
    SaveScreenshot(
        f"{job_directory}/cp-contour-bottom.png",
        renderView,
        ImageResolution=renderView.ViewSize,
    )

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    ResetSession()
