# typer
import typer

# commands - reset
from commands.reset_case_template import reset_case_template
from commands.reset_output import reset_output

# commands - check
from commands.check_output import check_output
from commands.check_config import check_config
from commands.check_meshes import check_meshes
from commands.check_geometries import check_geometries
from commands.check_cases import check_cases
from commands.check_setup import check_setup
from commands.check_run import check_run
from commands.check_assets import check_assets

# commands - execution
from commands.run import run
from commands.doe import doe

# commands - collect
from commands.collect_assets import collect_assets

# commands - random
from commands.test import test
from commands.hello import hello

app = typer.Typer(name="pfo", help="Opensource Parametric Flow Optimizer")

# reset
app.command(
    name="resetCaseTemplate",
    help="Resets the case template directory in `input/case_template` back to original settings. (WARNING: Your progress will be lost)",
)(reset_case_template)
app.command(
    name="resetOutput",
    help="Resets the output directory in `output/` back to original settings. (WARNING: Your progress will be lost)",
)(reset_output)

# checks
app.command(name="checkOutput")(check_output)
app.command(name="checkConfig")(check_config)
app.command(name="checkSetup")(check_setup)
app.command(name="checkGeometries")(check_geometries)
app.command(name="checkCases")(check_cases)
app.command(name="checkMeshes")(check_meshes)
app.command(name="checkRun")(check_run)
app.command(name="checkAssets")(check_assets)

# execution
app.command(name="run")(run)
app.command(name="doe")(doe)

# collect
app.command(name="collectAssets")(collect_assets)

# random
app.command(name="test")(test)
app.command(name="hello")(hello)

# report


@app.command()
def version():
    typer.echo("OpenPFO v0.1.0")


if __name__ == "__main__":
    app()
