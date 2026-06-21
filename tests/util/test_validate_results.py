import copy
import pytest
from util.validate_results import (
    validate_config,
    validate_parameter,
    validate_objective,
    validate_variable,
    validate_point,
    validate_step,
    validate_job,
    validate_solution,
    validate_search,
)


# ─────────────────────────────────────────────────────────────────────────────
# Canonical valid fixtures
# ─────────────────────────────────────────────────────────────────────────────

VALID_CONFIG_LOCAL = {
    "compute": {"hpc": False, "processors_per_job": 1, "max_job_workers": 1},
    "model": {
        "parameters": [{"id": "alpha", "name": "alpha", "min": 0.0, "max": 10.0}]
    },
    "optimizer": {"objectives": [{"id": "drag", "name": "drag", "type": "minimize"}]},
}

VALID_CONFIG_HPC = {
    "compute": {"hpc": True, "processors_per_job": 4, "max_job_workers": 2},
    "model": {
        "parameters": [{"id": "alpha", "name": "alpha", "min": 0.0, "max": 10.0}]
    },
    "optimizer": {"objectives": [{"id": "drag", "name": "drag", "type": "minimize"}]},
}

VALID_VARIABLE = {"id": "alpha", "name": "alpha", "value": 5.0}

VALID_POINT = {
    "representation": "(alpha: 5.0)",
    "variables": [VALID_VARIABLE],
}

VALID_STEP = {
    "id": "geometry",
    "runOk": True,
    "startTime": "2024-01-01T12:00:00",
    "endTime": "2024-01-01T12:00:30",
    "executionTimeSeconds": 30.0,
}

VALID_OBJECTIVE = {"id": "drag", "name": "drag", "type": "minimize", "value": 0.03}

VALID_PARAMETER = {
    "id": "alpha",
    "name": "alpha",
    "min": 0.0,
    "max": 10.0,
    "value": 5.0,
}

VALID_JOB = {
    "id": "job-0",
    "status": "complete",
    "searchId": "search-0",
    "runOk": True,
    "steps": [VALID_STEP],
    "startTime": "2024-01-01T12:00:00",
    "endTime": "2024-01-01T12:01:00",
    "jobDirectory": "output/job-0",
    "objectives": [VALID_OBJECTIVE],
    "meta": {},
    "point": VALID_POINT,
}

VALID_SOLUTION = {"point": VALID_POINT, "objectives": [VALID_OBJECTIVE]}

VALID_SEARCH = {"id": "search-0", "jobs": ["job-0", "job-1"]}


def _drop(d: dict, key: str) -> dict:
    """Return a shallow copy of d with key removed."""
    c = copy.deepcopy(d)
    del c[key]
    return c


def _set(d: dict, key: str, value) -> dict:
    """Return a shallow copy of d with key set to value."""
    c = copy.deepcopy(d)
    c[key] = value
    return c


# ─────────────────────────────────────────────────────────────────────────────
# validate_config — hpc=False (local)
# ─────────────────────────────────────────────────────────────────────────────


class TestValidateConfigLocal:
    def test_valid_local_config(self):
        assert validate_config(VALID_CONFIG_LOCAL) is None

    def test_missing_compute_section(self):
        with pytest.raises(SystemExit):
            validate_config(_drop(VALID_CONFIG_LOCAL, "compute"))

    def test_missing_hpc_key(self):
        c = copy.deepcopy(VALID_CONFIG_LOCAL)
        del c["compute"]["hpc"]
        with pytest.raises(SystemExit):
            validate_config(c)

    def test_hpc_not_bool(self):
        c = copy.deepcopy(VALID_CONFIG_LOCAL)
        c["compute"]["hpc"] = "false"
        with pytest.raises(SystemExit):
            validate_config(c)

    def test_missing_processors_per_job(self):
        c = copy.deepcopy(VALID_CONFIG_LOCAL)
        del c["compute"]["processors_per_job"]
        with pytest.raises(SystemExit):
            validate_config(c)

    def test_processors_per_job_not_int(self):
        c = copy.deepcopy(VALID_CONFIG_LOCAL)
        c["compute"]["processors_per_job"] = 1.5
        with pytest.raises(SystemExit):
            validate_config(c)

    def test_missing_max_job_workers(self):
        c = copy.deepcopy(VALID_CONFIG_LOCAL)
        del c["compute"]["max_job_workers"]
        with pytest.raises(SystemExit):
            validate_config(c)

    def test_missing_model_section(self):
        with pytest.raises(SystemExit):
            validate_config(_drop(VALID_CONFIG_LOCAL, "model"))

    def test_missing_parameters_list(self):
        c = copy.deepcopy(VALID_CONFIG_LOCAL)
        del c["model"]["parameters"]
        with pytest.raises(SystemExit):
            validate_config(c)

    def test_missing_optimizer_section(self):
        with pytest.raises(SystemExit):
            validate_config(_drop(VALID_CONFIG_LOCAL, "optimizer"))

    def test_missing_objectives_list(self):
        c = copy.deepcopy(VALID_CONFIG_LOCAL)
        del c["optimizer"]["objectives"]
        with pytest.raises(SystemExit):
            validate_config(c)

    @pytest.mark.parametrize("invalid_type", ["min", "max", "Minimize", "MAXIMIZE", ""])
    def test_objective_invalid_type_is_rejected(self, invalid_type):
        c = copy.deepcopy(VALID_CONFIG_LOCAL)
        c["optimizer"]["objectives"][0]["type"] = invalid_type
        with pytest.raises(SystemExit):
            validate_config(c)


# ─────────────────────────────────────────────────────────────────────────────
# validate_config — hpc=True (HPC)
# ─────────────────────────────────────────────────────────────────────────────


class TestValidateConfigHPC:
    def test_valid_hpc_config(self):
        assert validate_config(VALID_CONFIG_HPC) is None

    def test_hpc_true_is_accepted(self):
        """hpc=True is a valid boolean and must not trigger sys.exit."""
        c = copy.deepcopy(VALID_CONFIG_HPC)
        assert validate_config(c) is None

    def test_hpc_false_and_hpc_true_both_valid(self):
        assert validate_config(VALID_CONFIG_LOCAL) is None
        assert validate_config(VALID_CONFIG_HPC) is None

    def test_hpc_string_true_is_rejected(self):
        c = copy.deepcopy(VALID_CONFIG_HPC)
        c["compute"]["hpc"] = "true"
        with pytest.raises(SystemExit):
            validate_config(c)

    def test_hpc_integer_one_is_rejected(self):
        c = copy.deepcopy(VALID_CONFIG_HPC)
        c["compute"]["hpc"] = 1
        with pytest.raises(SystemExit):
            validate_config(c)

    @pytest.mark.parametrize("invalid_type", ["min", "max", "Minimize", "MAXIMIZE", ""])
    def test_objective_invalid_type_is_rejected(self, invalid_type):
        c = copy.deepcopy(VALID_CONFIG_HPC)
        c["optimizer"]["objectives"][0]["type"] = invalid_type
        with pytest.raises(SystemExit):
            validate_config(c)


# ─────────────────────────────────────────────────────────────────────────────
# validate_parameter
# ─────────────────────────────────────────────────────────────────────────────


class TestValidateParameter:
    def test_valid_parameter(self):
        assert validate_parameter(VALID_PARAMETER) is None

    @pytest.mark.parametrize("field", ["id", "name", "min", "max", "value"])
    def test_missing_field(self, field):
        with pytest.raises(SystemExit):
            validate_parameter(_drop(VALID_PARAMETER, field))

    def test_id_not_string(self):
        with pytest.raises(SystemExit):
            validate_parameter(_set(VALID_PARAMETER, "id", 123))

    def test_min_accepts_int(self):
        assert validate_parameter(_set(VALID_PARAMETER, "min", 0)) is None

    def test_value_none_is_rejected(self):
        """Parameters in results.json must have a concrete value, not None."""
        with pytest.raises(SystemExit):
            validate_parameter(_set(VALID_PARAMETER, "value", None))


# ─────────────────────────────────────────────────────────────────────────────
# validate_objective
# ─────────────────────────────────────────────────────────────────────────────


class TestValidateObjective:
    def test_valid_objective_with_value(self):
        assert validate_objective(VALID_OBJECTIVE) is None

    def test_valid_objective_with_none_value(self):
        assert validate_objective(_set(VALID_OBJECTIVE, "value", None)) is None

    @pytest.mark.parametrize("field", ["id", "name", "type", "value"])
    def test_missing_field(self, field):
        with pytest.raises(SystemExit):
            validate_objective(_drop(VALID_OBJECTIVE, field))

    def test_value_string_is_rejected(self):
        with pytest.raises(SystemExit):
            validate_objective(_set(VALID_OBJECTIVE, "value", "0.03"))

    @pytest.mark.parametrize("valid_type", ["minimize", "maximize"])
    def test_valid_types_are_accepted(self, valid_type):
        assert validate_objective(_set(VALID_OBJECTIVE, "type", valid_type)) is None

    @pytest.mark.parametrize("invalid_type", ["min", "max", "Minimize", "MAXIMIZE", ""])
    def test_invalid_type_strings_are_rejected(self, invalid_type):
        with pytest.raises(SystemExit):
            validate_objective(_set(VALID_OBJECTIVE, "type", invalid_type))


# ─────────────────────────────────────────────────────────────────────────────
# validate_variable
# ─────────────────────────────────────────────────────────────────────────────


class TestValidateVariable:
    def test_valid_variable(self):
        assert validate_variable(VALID_VARIABLE) is None

    @pytest.mark.parametrize("field", ["id", "name", "value"])
    def test_missing_field(self, field):
        with pytest.raises(SystemExit):
            validate_variable(_drop(VALID_VARIABLE, field))

    def test_value_string_is_rejected(self):
        with pytest.raises(SystemExit):
            validate_variable(_set(VALID_VARIABLE, "value", "5.0"))

    def test_value_int_is_accepted(self):
        assert validate_variable(_set(VALID_VARIABLE, "value", 5)) is None


# ─────────────────────────────────────────────────────────────────────────────
# validate_point
# ─────────────────────────────────────────────────────────────────────────────


class TestValidatePoint:
    def test_valid_point(self):
        assert validate_point(VALID_POINT) is None

    def test_missing_representation(self):
        with pytest.raises(SystemExit):
            validate_point(_drop(VALID_POINT, "representation"))

    def test_missing_variables(self):
        with pytest.raises(SystemExit):
            validate_point(_drop(VALID_POINT, "variables"))

    def test_invalid_variable_inside_point(self):
        p = copy.deepcopy(VALID_POINT)
        p["variables"][0]["value"] = "bad"
        with pytest.raises(SystemExit):
            validate_point(p)


# ─────────────────────────────────────────────────────────────────────────────
# validate_step
# ─────────────────────────────────────────────────────────────────────────────


class TestValidateStep:
    def test_valid_step(self):
        assert validate_step(VALID_STEP) is None

    @pytest.mark.parametrize(
        "field", ["id", "runOk", "startTime", "endTime", "executionTimeSeconds"]
    )
    def test_missing_field(self, field):
        with pytest.raises(SystemExit):
            validate_step(_drop(VALID_STEP, field))

    def test_run_ok_not_bool(self):
        with pytest.raises(SystemExit):
            validate_step(_set(VALID_STEP, "runOk", 1))

    def test_execution_time_int_is_accepted(self):
        assert validate_step(_set(VALID_STEP, "executionTimeSeconds", 30)) is None


# ─────────────────────────────────────────────────────────────────────────────
# validate_job
# ─────────────────────────────────────────────────────────────────────────────


class TestValidateJob:
    def test_valid_job(self):
        assert validate_job(VALID_JOB) is None

    @pytest.mark.parametrize(
        "field",
        [
            "id",
            "status",
            "searchId",
            "runOk",
            "steps",
            "startTime",
            "endTime",
            "jobDirectory",
            "objectives",
            "meta",
            "point",
        ],
    )
    def test_missing_field(self, field):
        with pytest.raises(SystemExit):
            validate_job(_drop(VALID_JOB, field))

    def test_invalid_step_inside_job(self):
        j = copy.deepcopy(VALID_JOB)
        del j["steps"][0]["runOk"]
        with pytest.raises(SystemExit):
            validate_job(j)

    def test_invalid_objective_inside_job(self):
        j = copy.deepcopy(VALID_JOB)
        j["objectives"][0]["value"] = "bad"
        with pytest.raises(SystemExit):
            validate_job(j)


# ─────────────────────────────────────────────────────────────────────────────
# validate_solution
# ─────────────────────────────────────────────────────────────────────────────


class TestValidateSolution:
    def test_valid_solution(self):
        assert validate_solution(VALID_SOLUTION) is None

    def test_missing_point(self):
        with pytest.raises(SystemExit):
            validate_solution(_drop(VALID_SOLUTION, "point"))

    def test_missing_objectives(self):
        with pytest.raises(SystemExit):
            validate_solution(_drop(VALID_SOLUTION, "objectives"))

    def test_solution_not_dict(self):
        with pytest.raises(SystemExit):
            validate_solution("not a dict")

    def test_invalid_objective_inside_solution(self):
        s = copy.deepcopy(VALID_SOLUTION)
        s["objectives"][0]["value"] = "bad"
        with pytest.raises(SystemExit):
            validate_solution(s)


# ─────────────────────────────────────────────────────────────────────────────
# validate_search
# ─────────────────────────────────────────────────────────────────────────────


class TestValidateSearch:
    def test_valid_search(self):
        assert validate_search(VALID_SEARCH) is None

    def test_missing_id(self):
        with pytest.raises(SystemExit):
            validate_search(_drop(VALID_SEARCH, "id"))

    def test_missing_jobs(self):
        with pytest.raises(SystemExit):
            validate_search(_drop(VALID_SEARCH, "jobs"))

    def test_search_not_dict(self):
        with pytest.raises(SystemExit):
            validate_search("not a dict")

    def test_job_id_not_string(self):
        s = copy.deepcopy(VALID_SEARCH)
        s["jobs"] = [123]
        with pytest.raises(SystemExit):
            validate_search(s)
