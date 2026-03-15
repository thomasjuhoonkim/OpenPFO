# system
import glob
import os
import shutil

# imageio
from PIL import Image

# typer
import typer
from typing_extensions import Annotated

# constants
from constants.path import COLLECT_ASSETS_DIRECTORY, OUTPUT_DIRECTORY


def collect_assets(
    asset: Annotated[
        str, typer.Argument(help="File name and extension of asset")
    ] = True,
    gif: Annotated[
        bool,
        typer.Option(help="Create a GIF of the assets (only available for images)"),
    ] = False,
    duration: Annotated[
        float,
        typer.Option(help="Duration of each frame in the GIF (in seconds)"),
    ] = 250,
):
    split = asset.split(".")
    asset_name, asset_ext = split

    if len(split) != 2 or not asset_name or not asset_ext:
        print("Invalid asset")

    jobs = os.listdir(OUTPUT_DIRECTORY)
    jobs.sort()

    if ".DS_Store" in jobs:
        jobs.remove(".DS_Store")

    os.makedirs(f"{COLLECT_ASSETS_DIRECTORY}/{asset_name}", exist_ok=True)

    for job in jobs:
        original = f"{OUTPUT_DIRECTORY}/{job}/{asset_name}.{asset_ext}"
        if os.path.isfile(original):
            dest = shutil.copy(
                original, f"{COLLECT_ASSETS_DIRECTORY}/{asset_name}/{job}.{asset_ext}"
            )
            print(dest)

    if gif:
        print("Reading images for GIF generation...")

        if asset_ext not in ["png", "jpg", "jpeg"]:
            print("GIF creation is only available for images")
            return

        images = []
        for collected_asset in sorted(
            glob.glob(f"{COLLECT_ASSETS_DIRECTORY}/{asset_name}/*.{asset_ext}")
        ):
            temp = Image.open(collected_asset)
            images.append(temp.copy())
            temp.close()
            print("Read file:", collected_asset)

        images[0].save(
            fp=f"{COLLECT_ASSETS_DIRECTORY}/{asset_name}.gif",
            format="GIF",
            append_images=images[1:],
            save_all=True,
            duration=duration,
            loop=0,
        )

        print("Saved GIF to:", f"{COLLECT_ASSETS_DIRECTORY}/{asset_name}.gif")
