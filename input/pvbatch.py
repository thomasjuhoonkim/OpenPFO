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
    reader = OpenDataFile(input_filepath)
    VIEW_SIZE = [3840, 2160]

    # ==========================================================================
    renderView1 = CreateView("RenderView")
    renderView1.ViewSize = VIEW_SIZE

    display1 = Show(reader, renderView1)
    # display1.Representation = "Surface With Edges"

    renderView1.CameraPosition = [-0.1, 5, 0]
    renderView1.CameraFocalPoint = [-0.1, 0, 0]
    renderView1.CameraViewUp = [0, 0, 1]

    Render()

    SaveScreenshot(
        f"{assets_directory}/mesh.png",
        renderView1,
        ImageResolution=renderView1.ViewSize,
    )
    # ==========================================================================
    renderView2 = CreateView("RenderView")
    renderView2.ViewSize = VIEW_SIZE

    slice = Slice(Input=reader)
    slice.SliceType = "Plane"
    slice.SliceType.Origin = [0, 0, 0.05]
    slice.SliceType.Normal = [0, 0, 1]
    # slice.Crinkleslice = True

    display2 = Show(slice, renderView2)
    # display2.Representation = "Surface With Edges"

    renderView2.CameraPosition = [-0.1, -0.5, 5]
    renderView2.CameraFocalPoint = [-0.1, -0.5, 0]
    renderView2.CameraViewUp = [0, 1, 0]

    Render()

    SaveScreenshot(
        f"{assets_directory}/slice.png",
        renderView2,
        ImageResolution=renderView2.ViewSize,
    )

    # ==========================================================================

    ResetSession()
