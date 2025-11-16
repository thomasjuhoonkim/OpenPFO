import typer

from commands.reset_input_case_template import reset_input_case_template
from commands.reset_output import reset_output

from commands.check_output import check_output
from commands.check_meshes import check_meshes
from commands.check_model import check_model
from commands.check_setup import check_setup

from commands.test import test

from commands.run import run

app = typer.Typer(name="pfo", help="Opensource Parametric Flow Optimizer")

# reset
app.command(
    name="resetInputCaseTemplate",
    help="Resets the case template directory in `input/case_template` back to original settings. (WARNING: Your progress will be lost)",
)(reset_input_case_template)
app.command(
    name="resetOutput",
    help="Resets the output directory in `output/` back to original settings. (WARNING: Your progress will be lost)",
)(reset_output)

# checks
app.command(name="checkOutput")(check_output)
app.command(name="checkSetup")(check_setup)
app.command(name="checkMeshes")(check_meshes)
app.command(name="checkModel")(check_model)

# run
app.command(name="run")(run)

app.command(name="test")(test)

# report


@app.command()
def version():
    typer.echo("OpenPFO v0.1.0")


if __name__ == "__main__":
    app()
