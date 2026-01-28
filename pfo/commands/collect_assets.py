# system
import os
import shutil

# typer
import typer
from typing_extensions import Annotated

# constants
from constants.path import COLLECT_ASSETS_DIRECTORY, OUTPUT_DIRECTORY


def collect_assets(
    asset: Annotated[
        str, typer.Argument(help="File name and extension of asset")
    ] = True,
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
