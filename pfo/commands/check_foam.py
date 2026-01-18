# system
import subprocess

# util
from util.get_logger import get_logger

logger = get_logger()


def check_foam():
    try:
        subprocess.run(["foamVersion"], capture_output=True, text=True, check=True)
    except Exception:
        logger.exception(
            "OpenFOAM is invalid. Have you initialized the OpenFOAM environment?"
        )
