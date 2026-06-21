from util.get_pfo_command import get_pfo_command


class TestGetPfoCommand:
    def test_joins_argv_with_spaces(self):
        assert get_pfo_command(["pfo", "run", "--resume"]) == "pfo run --resume"

    def test_single_element(self):
        assert get_pfo_command(["pfo"]) == "pfo"

    def test_empty_argv(self):
        assert get_pfo_command([]) == ""

    def test_preserves_order(self):
        assert get_pfo_command(["pfo", "checkRun", "--count", "5"]) == "pfo checkRun --count 5"
