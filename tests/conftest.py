import sys
import os

# ── 1. Make pfo/ importable ────────────────────────────────────────────────
_PFO_PATH = os.path.join(os.path.dirname(__file__), "..", "pfo")
if _PFO_PATH not in sys.path:
    sys.path.insert(0, _PFO_PATH)

# ── 2. Replace get_config() before any downstream module is imported ────────
#    Modules like util.get_config_parameters run `config = get_config()` at
#    module level, so the mock must be installed before they are first imported.
MOCK_CONFIG = {
    "compute": {
        "hpc": False,
        "processors_per_job": 1,
        "max_job_workers": 1,
    },
    "model": {
        "parameters": [
            {"name": "alpha", "id": "alpha", "min": 0.0, "max": 10.0},
            {"name": "beta", "id": "beta", "min": 1.0, "max": 5.0},
        ]
    },
    "optimizer": {
        "objectives": [
            {"name": "drag", "id": "drag", "type": "minimize"},
            {"name": "lift", "id": "lift", "type": "maximize"},
        ]
    },
}

import util.get_config as _get_config_module  # noqa: E402

_get_config_module.get_config = lambda: MOCK_CONFIG
