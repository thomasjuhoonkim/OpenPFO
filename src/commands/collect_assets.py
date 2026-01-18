# system
import os
import shutil

# typer
import typer
from typing_extensions import Annotated

# constants
from constants.path import COLLECT_ASSETS_DIRECTORY, OUTPUT_ASSETS_DIRECTORY


def collect_assets(
    asset: Annotated[
        str, typer.Argument(help="File name and extension of asset")
    ] = True,
):
    split = asset.split(".")
    asset_name, asset_ext = split

    if len(split) != 2 or not asset_name or not asset_ext:
        print("Invalid asset")

    cases = os.listdir(OUTPUT_ASSETS_DIRECTORY)
    cases.sort()

    if ".DS_Store" in cases:
        cases.remove(".DS_Store")

    os.makedirs(f"{COLLECT_ASSETS_DIRECTORY}/{asset_name}", exist_ok=True)

    for case in cases:
        original = f"{OUTPUT_ASSETS_DIRECTORY}/{case}/{asset_name}.{asset_ext}"
        if os.path.isfile(original):
            dest = shutil.copy(
                original, f"{COLLECT_ASSETS_DIRECTORY}/{asset_name}/{case}.{asset_ext}"
            )
            print(dest)
