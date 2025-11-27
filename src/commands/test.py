import os
import shutil


def test():
    cases = os.listdir("output/assets")
    cases.remove(".DS_Store")
    os.makedirs("temp", exist_ok=True)

    for i, case in enumerate(cases):
        original = f"output/assets/{case}/mesh.png"
        dest = shutil.copy(original, f"temp/{i}.png")
        print(dest)
