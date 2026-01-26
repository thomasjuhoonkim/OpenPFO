import sys

from paraview.simple import *

paraview.simple._DisableFirstRenderCameraReset()

if __name__ == "__main__":
    # validate inputs
    if len(sys.argv) < 3:
        print("Usage: pvbatch -- script.py <input_filepath> <assets_directory>")
        sys.exit(1)

    # parse inputs
    input_filepath = sys.argv[1]
    assets_directory = sys.argv[2]

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

    pLUT = GetColorTransferFunction("p")
    HideScalarBarIfNotNeeded(pLUT, renderView)

    calculator1 = Calculator(registrationName="Calculator1", Input=parafoam)

    calculator1.Set(
        ResultArrayName="Cp",
        Function="= (p - 0)/(0.5*1.225*(10^2))",
    )
    calculator1.AttributeType = "Cell Data"

    display1 = Show(calculator1, renderView, "GeometryRepresentation")
    display1.RescaleTransferFunctionToDataRange(True, False)
    display1.SetScalarBarVisibility(renderView, True)
    display1.Representation = "Surface"

    Hide(parafoam, renderView)

    ColorBy(display1, ("CELLS", "Cp"))

    cpLUT = GetColorTransferFunction("Cp")

    Render()

    SaveScreenshot(
        f"{assets_directory}/cp-contour.png",
        renderView,
        ImageResolution=renderView.ViewSize,
    )

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    ResetSession()
