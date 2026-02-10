# system
import subprocess
import concurrent.futures

# util
from util.get_logger import get_logger

logger = get_logger()


def run_parallel_commands(commands, max_workers=None):
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(subprocess.run, cmd.split(), capture_output=True, text=True)
            for cmd in commands
        ]

        # Wait for all futures to complete and get results
        results = []
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                logger.info(
                    f"Command '{' '.join(result.args)}' finished with return code: {result.returncode}"
                )
                logger.info(result.stderr)
                results.append(result)
            except BaseException:
                logger.exception(
                    f"An exception occurred while running command {' '.join(result.args)}"
                )

    logger.info("All commands have finished execution.")
    return results
