import click, os, shutil
from .server import run_dev_server

@click.group()
def cli():
    pass

def download_boilerplate(target_dir):
    from git import Repo
    # git clone to tmp dir
    temp_dir = os.path.join(target_dir, "tmp")
    Repo.clone_from("https://github.com/bananaml/banana-cli.git", temp_dir)
    
    # move boilerplate to current dir
    boilerplate_path = os.path.join(temp_dir, "boilerplate/potassium")
    files = os.listdir(boilerplate_path)
    for f in files:
        src_path = os.path.join(boilerplate_path, f)
        dst_path = os.path.join(target_dir, f)
        shutil.move(src_path, dst_path)
    
    # remove temp dir
    shutil.rmtree(temp_dir)

def get_target_dir(dir):
    # route to cwd if no path specified
    if len(dir) == 0:
        target_dir = "."
    else:
        target_dir = dir[0]
    # clean to relative path from here
    target_dir = os.path.relpath(target_dir)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    return target_dir

@click.command()
@click.argument('path', type=click.Path(exists=False, dir_okay=True, file_okay=False), nargs=-1)
def init(path):
    click.echo('⏰ Downloading boilerplate...')
    target_dir = get_target_dir(path)
    download_boilerplate(target_dir)
    click.echo('\n🍌 Project ready to go (hurrah!)')
    click.echo('\n💨 To run the server manually, run:')
    click.echo('python3 -m venv venv')
    click.echo('. ./venv/bin/activate')
    click.echo('pip3 install -r requirements.txt')
    click.echo('python3 app.py')
    click.echo('\n🔥 To run a dev server with hot-reload, run:')
    click.echo('banana dev')

def get_app_path(entrypoint):
    # route to cwd if no path specified
    if len(entrypoint) == 0:
        app_path = "."
    else:
        app_path = entrypoint[0]
    # if dir specified, route to app.py within that dir
    dir_path = ""
    if os.path.isdir(app_path):
        dir_path = app_path
        app_path = os.path.join(dir_path, "app.py")
    # clean to relative path from here
    app_path = os.path.relpath(app_path)
    if not os.path.exists(app_path):
        raise click.UsageError("app.py not found in directory: " + os.path.abspath(dir_path) + "\n\nIf using an entrypoint other than app.py, specify it by name with `banana dev path/to/entrypoint.py`\nIf starting a new project, run `banana init`")
    return app_path

@click.command()
@click.argument('entrypoint', type=click.Path(exists=True), nargs=-1)
def dev(entrypoint):
    app_path = get_app_path(entrypoint)
    run_dev_server(app_path)

@click.command()
def test():
    click.echo('Stub: would run unit tests.')

@click.command()
def build():
    click.echo('Stub: would verify build')


cli.add_command(init)
cli.add_command(dev)
cli.add_command(test)
cli.add_command(build)

if __name__ == "__main__":
    cli()