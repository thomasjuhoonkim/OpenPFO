from unittest.mock import MagicMock


def mock_parameters():
    """Two Parameter mocks matching the MOCK_CONFIG in tests/conftest.py."""
    alpha = MagicMock()
    alpha.get_name.return_value = "alpha"
    alpha.get_id.return_value = "alpha"
    alpha.get_min.return_value = 0.0
    alpha.get_max.return_value = 10.0

    beta = MagicMock()
    beta.get_name.return_value = "beta"
    beta.get_id.return_value = "beta"
    beta.get_min.return_value = 1.0
    beta.get_max.return_value = 5.0

    return [alpha, beta]
