import click, os

@click.group()
def cli():
    pass

@click.command()
def init():
    
    click.echo('Initialized the project')

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
    click.echo('Stub: would start interractive dev server on ' + app_path)

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