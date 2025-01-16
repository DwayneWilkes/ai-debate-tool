import subprocess
import click
import sys

PYTHON_EXECUTABLE = sys.executable
DOCKER_IMAGE_NAME = "ai-debate-backend"
DOCKERFILE_PATH = "backend/Dockerfile"
TESTS_PATH = "backend/tests"

TASKS = {
    "run-app": {
        "description": "Run the Flask application.",
        "command": [PYTHON_EXECUTABLE, "-m", "backend.app.main"],
    },
    "run-tests": {
        "description": "Run tests with pytest.",
        "command": [PYTHON_EXECUTABLE, "-m", "pytest", TESTS_PATH],
    },
    "build-image": {
        "description": "Build the Docker image.",
        "command": ["docker", "build", "-t", DOCKER_IMAGE_NAME, "-f", DOCKERFILE_PATH, "."],
    },
    "run-image": {
        "description": "Run the Docker container.",
        "command": ["docker", "run", "-p", "5000:5000", DOCKER_IMAGE_NAME],
    },
    "run-image-interactive": {
        "description": "Run the Docker container interactively.",
        "command": ["docker", "run", "-it", "-p", "5000:5000", DOCKER_IMAGE_NAME],
    },
}


class AliasedGroup(click.Group):
    """Custom Click group to support command aliases."""

    aliases = {
        "r": "run-app",
        "t": "run-tests",
        "b": "build-image",
        "i": "run-image",
        "a": "all",
    }

    def get_command(self, ctx, cmd_name):
        # Map short aliases to their respective commands
        cmd_name = self.aliases.get(cmd_name, cmd_name)
        return super().get_command(ctx, cmd_name)


def common_options(func):
    """Decorator to add common options to all commands."""
    func = click.option("--dry-run", "-dr", is_flag=True, help="Preview commands without executing them.")(func)
    func = click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging.")(func)
    return func


@click.group(cls=AliasedGroup)
def cli():
    """CLI tool to manage the AI Debate Tool project."""
    pass


def run_command(command, dry_run=False, verbose=False):
    """Run a shell command with optional dry-run and verbose modes."""
    if verbose:
        click.echo(f"Executing: {' '.join(command)}")
    if dry_run:
        click.echo(f"[DRY-RUN] {' '.join(command)}")
        return
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        click.echo(f"Error occurred while executing a command: {e}", err=True)
        sys.exit(e.returncode)
    except FileNotFoundError as e:
        click.echo(f"Command not found: {e}", err=True)
        sys.exit(127)
    except Exception as e:
        click.echo(f"An unexpected error occurred: {e}", err=True)
        sys.exit(1)


@cli.command("run-app", help=TASKS["run-app"]["description"])
@common_options
def run_app(dry_run, verbose):
    """Run the Flask application."""
    run_command(TASKS["run-app"]["command"], dry_run=dry_run, verbose=verbose)


@cli.command("run-tests", help=TASKS["run-tests"]["description"])
@common_options
def run_tests(dry_run, verbose):
    """Run tests with pytest."""
    run_command(TASKS["run-tests"]["command"], dry_run=dry_run, verbose=verbose)


@cli.command("build-image", help=TASKS["build-image"]["description"])
@common_options
def build_image(dry_run, verbose):
    """Build the Docker image."""
    run_command(TASKS["build-image"]["command"], dry_run=dry_run, verbose=verbose)


@cli.command("run-image", help=TASKS["run-image"]["description"])
@click.option("-I", "--interactive", is_flag=True, help=TASKS["run-image-interactive"]["description"])
@common_options
def run_image(dry_run, verbose, interactive):
    """Run the Docker container."""
    mode = "run-image-interactive" if interactive else "run-image"
    run_command(TASKS[mode]["command"], dry_run=dry_run, verbose=verbose)


@cli.command("all", help="Run all tasks: tests, build Docker image, and run the container.")
@common_options
def all_tasks(dry_run, verbose):
    """Run all tasks: tests, build Docker image, and run the container."""
    try:
        for task in ["run-tests", "build-image", "run-image"]:
            run_command(TASKS[task]["command"], dry_run=dry_run, verbose=verbose)
    except SystemExit as e:
        click.echo("Stopping execution due to a failure.", err=True)
        sys.exit(e.code)


if __name__ == "__main__":
    cli()
