# click is our CLI library
import click
import os

# local imports
from .cmd_dev import run_dev_server
from .utils import get_target_dir, get_app_path, get_site_packages, download_boilerplate, create_venv, install_venv

@click.group()
def cli():
    pass

@click.command()
@click.argument('path', type=click.Path(exists=False, dir_okay=True, file_okay=False), nargs=-1)
@click.option('--no-venv', is_flag=True, required=False, help="Disable automatic use of a virtual environment")
@click.option('--no-install', is_flag=True, required=False, help="Disable automatic install of requirements.txt")
def init(path, no_venv, no_install):
    click.echo('⏰ Downloading boilerplate...')
    target_dir = get_target_dir(path)
    if target_dir == ".":
        # verify they're not installing into an existing dir
        if len(os.listdir(target_dir)) > 0:
            click.confirm("This is not an empty directory, and the install may overwrite existing files.\nDo you want to proceed?", abort=True)
    download_boilerplate(target_dir)
    if not no_venv:
        click.echo('🌎 Creating virtual environment...')
        venv_path = os.path.join(target_dir, "venv")
        create_venv(venv_path)

        if not no_install:
            click.echo('📦 Downloading packages...')
            req_path = os.path.join(target_dir, "requirements.txt")
            install_venv(req_path, venv_path)

    click.echo('\n🍌 Project ready to go (hurrah!)')
    click.echo('\n🔥 To run a dev server with hot-reload, run:')
    if target_dir != ".":
        click.echo(f'cd {target_dir}')
    if no_install:
        click.echo(f'banana install')
    click.echo('banana dev')

@click.command()
@click.option('--venv', default="venv", required=False, type=str, help="The path of the virtual environment to install into. Defaults to venv.")
def install(venv):
    if not os.path.exists(venv):
        click.echo('🌎 Creating virtual environment...')
        create_venv(venv)
    click.echo('📦 Downloading packages...')
    install_venv("requirements.txt", venv)

@click.command()
@click.option('--venv', default="venv", required=False, type=str, help="The path of the virtual environment to run in. Defaults to venv.")
@click.option('--auto-compat', default=False, required=False, type=bool, help="Prevents cuda use if there is no GPU visible. Defaults to True.")
@click.argument('entrypoint', type=click.Path(exists=True), nargs=-1)
def dev(venv, auto_compat, entrypoint):
    app_path = get_app_path(entrypoint)
    site_packages = get_site_packages(app_path, venv_name = venv)
    run_dev_server(app_path, site_packages, auto_compat)

cli.add_command(init)
cli.add_command(install)
cli.add_command(dev)

if __name__ == "__main__":
    cli()