# typer
import typer

# commands - reset
from commands.reset_output import reset_output

# commands - check
from commands.check_objectives import check_objectives
from commands.check_geometries import check_geometries
from commands.check_cleanup import check_cleanup
from commands.check_results import check_results
from commands.check_prepare import check_prepare
from commands.check_solver import check_solver
from commands.check_output import check_output
from commands.check_config import check_config
from commands.check_meshes import check_meshes
from commands.check_run import check_run

# commands - execution
from commands.run import run

# commands - collect
from commands.collect_assets import collect_assets

# commands - random
from commands.test import test
from commands.hello import hello

app = typer.Typer(name="pfo", help="Open Parametric Flow Optimizer")

# reset
app.command(
    name="resetOutput",
    help="Resets the output directory in `output/` back to original settings. (WARNING: Your progress will be lost)",
)(reset_output)

# checks
app.command(name="checkConfig")(check_config)
app.command(name="checkPrepare")(check_prepare)
app.command(name="checkGeometries")(check_geometries)
app.command(name="checkMeshes")(check_meshes)
app.command(name="checkSolver")(check_solver)
app.command(name="checkObjectives")(check_objectives)
app.command(name="checkCleanup")(check_cleanup)
app.command(name="checkRun")(check_run)
app.command(name="checkResults")(check_results)
app.command(name="checkOutput")(check_output)

# execution
app.command(name="run")(run)

# collect
app.command(name="collectAssets")(collect_assets)

# random
app.command(name="test")(test)
app.command(name="hello")(hello)

# report


@app.command()
def version():
    typer.echo("OpenPFO v1.0.0")


if __name__ == "__main__":
    app()
