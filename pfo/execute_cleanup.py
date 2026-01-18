# system
import subprocess

# classes
from classes.functions import ExecuteCleanupParameters, ExecuteCleanupReturn


def execute_cleanup(
    execute_cleanup_parameters: ExecuteCleanupParameters,
) -> ExecuteCleanupReturn:
    """
    The execute_cleanup function used to clean up solver artifacts after each job.

    NOTE: This function does not return a value.
    """

    """ ======================= YOUR CODE BELOW HERE ======================= """

    case_directory = execute_cleanup_parameters.output_case_directory
    logger = execute_cleanup_parameters.logger
    commands = [
        f"pyFoamClearCase.py {case_directory} --keep-last --keep-postprocessing --processors-remove",
    ]

    run_ok = True
    for command in commands:
        try:
            subprocess.run(
                command.split(" "), capture_output=True, text=True, check=True
            )
            logger.info(f"Successfully cleaned up solver artifacts in {case_directory}")
        except subprocess.CalledProcessError as error:
            run_ok = False
            logger.error(f"{command} failed")
            logger.error(f"\n{error.stderr}")

    EXECUTE_CLEANUP_RETURN = ExecuteCleanupReturn(run_ok=run_ok)

    """ ======================= YOUR CODE ABOVE HERE ======================= """

    return EXECUTE_CLEANUP_RETURN
