# click is our CLI library
import click

# local imports
from .cmd_dev import run_dev_server
from .utils import get_target_dir, get_app_path, download_boilerplate

@click.group()
def cli():
    pass

@click.command()
@click.argument('path', type=click.Path(exists=False, dir_okay=True, file_okay=False), nargs=-1)
def init(path):
    click.echo('⏰ Downloading boilerplate...')
    target_dir = get_target_dir(path)
    download_boilerplate(target_dir)
    click.echo('\n🍌 Project ready to go (hurrah!)')
    click.echo('\n🔥 To run a dev server with hot-reload, run:')
    click.echo('banana dev')

@click.command()
@click.argument('entrypoint', type=click.Path(exists=True), nargs=-1)
def dev(entrypoint):
    app_path = get_app_path(entrypoint)
    run_dev_server(app_path)

cli.add_command(init)
cli.add_command(dev)

if __name__ == "__main__":
    cli()