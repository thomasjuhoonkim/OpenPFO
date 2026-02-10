# system
import sys

# util
from util.get_logger import get_logger

logger = get_logger()


def validate_parameter(parameter: dict):
    attributes = [
        ("id", str),
        ("name", str),
        ("min", (int, float)),
        ("max", (int, float)),
        ("value", (int, float)),
    ]

    for field, expected_type in attributes:
        if field not in parameter:
            logger.error(f'"{field}" is missing from parameter')
            sys.exit(1)
        if not isinstance(parameter[field], expected_type):
            logger.error(f'"{field}" in parameter is not {expected_type}')
            sys.exit(1)

    logger.info("Parameter is valid")

    return None


def validate_objective(objective: dict):
    attributes = [
        ("id", str),
        ("name", str),
        ("type", str),
        ("value", (int, float, type(None))),
    ]

    for field, expected_type in attributes:
        if field not in objective:
            logger.error(f'"{field}" is missing from objective')
            sys.exit(1)
        if not isinstance(objective[field], expected_type):
            logger.error(f'"{field}" in objective is not {expected_type}')
            sys.exit(1)

    logger.info("Objective is valid")

    return None


def validate_variable(variable: dict):
    attributes = [
        ("id", str),
        ("name", str),
        ("value", (int, float)),
    ]

    for field, expected_type in attributes:
        if field not in variable:
            logger.error(f'"{field}" is missing from variable')
            sys.exit(1)
        if not isinstance(variable[field], expected_type):
            logger.error(f'"{field}" in variable is not {expected_type}')
            sys.exit(1)

    return None


def validate_point(point: dict):
    attributes = [("representation", str), ("variables", list)]

    for field, expected_type in attributes:
        if field not in point:
            logger.error(f'"{field}" is missing from variable')
            sys.exit(1)
        if not isinstance(point[field], expected_type):
            logger.error(f'"{field}" in variable is not {expected_type}')
            sys.exit(1)

    for variable in point["variables"]:
        validate_variable(variable=variable)

    logger.info("Point is valid")

    return None


def validate_step(step: dict):
    attributes = [
        ("id", str),
        ("runOk", bool),
        ("startTime", str),
        ("endTime", str),
        ("executionTimeSeconds", (int, float)),
    ]

    for field, expected_type in attributes:
        if field not in step:
            logger.error(f'"{field}" is missing from step')
            sys.exit(1)
        if not isinstance(step[field], expected_type):
            logger.error(f'"{field}" in step is not {expected_type}')
            sys.exit(1)

    return None


def validate_job(job: dict):
    attributes = [
        ("id", str),
        ("status", str),
        ("searchId", str),
        ("runOk", bool),
        ("steps", list),
        ("startTime", str),
        ("endTime", str),
        ("jobDirectory", str),
        ("objectives", list),
        ("meta", dict),
    ]

    for field, expected_type in attributes:
        if field not in job:
            logger.error(f'"{field}" is missing from job')
            sys.exit(1)
        if not isinstance(job[field], expected_type):
            logger.error(f'"{field}" in job is not {expected_type}')
            sys.exit(1)

    for step in job["steps"]:
        validate_step(step)

    logger.info("Steps are valid")

    if "point" not in job:
        logger.error("point is missing from job")
        sys.exit(1)
    validate_point(point=job["point"])

    logger.info("Variables are valid")

    for objective in job["objectives"]:
        validate_objective(objective)

    logger.info("Objectives are valid")

    logger.info("Job is valid")

    return None


def validate_solution(solution: dict):
    if not isinstance(solution, dict):
        logger.error("solution is not a dict")
        sys.exit(1)

    attributes = [
        ("point", dict),
        ("objectives", list),
    ]

    for field, expected_type in attributes:
        if field not in solution:
            logger.error(f'"{field}" is missing from solution')
            sys.exit(1)
        if not isinstance(solution[field], expected_type):
            logger.error(f'"{field}" in solution is not {expected_type}')
            sys.exit(1)

    validate_point(solution["point"])

    logger.info("Point is valid")

    for objective in solution["objectives"]:
        validate_objective(objective)

    logger.info("Objectives are valid")

    return None


def validate_config(config: dict):
    # compute
    if "compute" not in config:
        logger.error("[compute] is missing")
        sys.exit(1)
    if "hpc" not in config["compute"]:
        logger.error("hpc is missing from [compute]")
        sys.exit(1)
    if not isinstance(config["compute"]["hpc"], bool):
        logger.error("hpc is not a boolean")
        sys.exit(1)
    if "processors_per_job" not in config["compute"]:
        logger.error("processors_per_job is missing from [compute]")
        sys.exit(1)
    if not isinstance(config["compute"]["processors_per_job"], int):
        logger.error("processors_per_job is not an integer")
        sys.exit(1)
    if "max_job_workers" not in config["compute"]:
        logger.error("max_job_workers is missing from [compute]")
        sys.exit(1)
    if not isinstance(config["compute"]["max_job_workers"], int):
        logger.error("max_job_workers is not an integer")
        sys.exit(1)

    if "model" not in config:
        logger.error("[model] is missing")
        sys.exit(1)
    if "parameters" not in config["model"]:
        logger.error("[[model.parameters]] is missing from [model]")
        sys.exit(1)
    if not isinstance(config["model"]["parameters"], list):
        logger.error("[[model.parameters]] is not a list")
        sys.exit(1)
    for parameter in config["model"]["parameters"]:
        attribtutes = [
            ("id", str),
            ("name", str),
            ("min", (int, float)),
            ("max", (int, float)),
        ]
        for attribute in attribtutes:
            field, type = attribute
            if not isinstance(parameter[field], type):
                logger.error(f'"{field}" in [[model.parameters]] is not {type}')
                sys.exit(1)

    if "optimizer" not in config:
        logger.error("[optimizer] is missing")
        sys.exit(1)
    if "objectives" not in config["optimizer"]:
        logger.error("[[optimizer.objectives]] is missing from [optimizer]")
        sys.exit(1)
    if not isinstance(config["optimizer"]["objectives"], list):
        logger.error("[[optimizer.objectives]] is not a list")
        sys.exit(1)
    for objective in config["optimizer"]["objectives"]:
        attribtutes = [("id", str), ("name", str), ("type", str)]
        for attribute in attribtutes:
            field, type = attribute
            if not isinstance(objective[field], type):
                logger.error(f'"{field}" in [[optimizer.objectives]] is not {type}')
                sys.exit(1)

    logger.info("Config is valid")

    return None


def validate_workflow(workflow: dict):
    if not isinstance(workflow, dict):
        logger.error("workflow is not a dict")
        sys.exit(1)

    if "jobs" not in workflow:
        logger.error("jobs is missing from workflow")
        sys.exit(1)
    if not isinstance(workflow["jobs"], list):
        logger.error("jobs is not a list")
        sys.exit(1)

    for job in workflow["jobs"]:
        validate_job(job)

    logger.info("Jobs are valid")

    if "searches" not in workflow:
        logger.error("searches is missing from workflow")
        sys.exit(1)
    if not isinstance(workflow["searches"], list):
        logger.error("searches is not a list")
        sys.exit(1)

    for search in workflow["searches"]:
        validate_search(search)

    logger.info("Searches are valid")

    logger.info("Workflow is valid")

    return None


def validate_search(search: dict):
    if not isinstance(search, dict):
        logger.error("search is not a dict")
        sys.exit(1)

    attributes = [
        ("id", str),
        ("jobs", list),
    ]

    for field, expected_type in attributes:
        if field not in search:
            logger.error(f'"{field}" is missing from search')
            sys.exit(1)
        if not isinstance(search[field], expected_type):
            logger.error(f'"{field}" in search is not {expected_type}')
            sys.exit(1)

    for job_id in search["jobs"]:
        if not isinstance(job_id, str):
            logger.error("job_id in search.jobs is not a string")
            sys.exit(1)

    logger.info("Job IDs are valid")

    logger.info("Search is valid")

    return None


def validate_results(results: dict):
    if not isinstance(results, dict):
        logger.error("results is not a dict")
        sys.exit(1)

    if "config" not in results:
        logger.error("config is missing from results")
        sys.exit(1)
    validate_config(results["config"])

    if "workflow" not in results:
        logger.error("workflow is missing from results")
        sys.exit(1)
    validate_workflow(results["workflow"])

    if "solutions" not in results:
        logger.error("solutions is missing from results")
        sys.exit(1)
    if not isinstance(results["solutions"], list):
        logger.error("solutions is not a list")
        sys.exit(1)

    for solution in results["solutions"]:
        validate_solution(solution)

    logger.info("Solutions are valid")

    attributes = [
        ("startTime", str),
        ("endTime", str),
        ("command", str),
    ]

    for field, expected_type in attributes:
        if field not in results:
            logger.error(f'"{field}" is missing from results')
            sys.exit(1)
        if not isinstance(results[field], expected_type):
            logger.error(f'"{field}" in results is not {expected_type}')
            sys.exit(1)

    logger.info("Results are valid")

    return None
