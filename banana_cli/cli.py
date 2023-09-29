# click is our CLI library
import click
import os
import requests

# local imports
from .cmd_dev import run_dev_server
from .utils import get_target_dir, get_app_path, get_site_packages, download_boilerplate, add_git, create_venv, install_venv
from .rick import roll

from yaspin import yaspin, Spinner
from prompt_toolkit import HTML, print_formatted_text
from prompt_toolkit.styles import Style

# override print with feature-rich ``print_formatted_text`` from prompt_toolkit
print = print_formatted_text

# build a basic prompt_toolkit style for styling the HTML wrapped text
style = Style.from_dict({
    'msg': '#4caf50 bold',
    'yay-msg': '#5aa02f italic',
    'err-msg': '#ff0000 bold',
})

__spinner = Spinner(["🍌  ", " 🍌 ", "  🍌", " 🍌 "], 200)

@click.group()
@click.version_option()
def cli():
    pass

@click.command()
@click.argument('path', type=click.Path(exists=False, dir_okay=True, file_okay=False), nargs=-1)
@click.option('--no-venv', is_flag=True, required=False, help="Disable automatic use of a virtual environment")
@click.option('--no-install', is_flag=True, required=False, help="Disable automatic install of requirements.txt")
@click.option('--no-git', is_flag=True, required=False, help="Disable automatic creation of a git repo")
def init(path, no_venv, no_install, no_git):
    target_dir = get_target_dir(path)

    # verify they're not installing into an existing dir
    if len(os.listdir(target_dir)) > 0:
        click.confirm("\nThis is not an empty directory, and the install may overwrite existing files.\nDo you want to proceed?", abort=True)

    with yaspin(__spinner) as sp:
        sp.text = 'Downloading boilerplate...'
        download_boilerplate(target_dir)
        with sp.hidden():
            print(HTML(u'✅   <yay-msg>Boilerplate downloaded</yay-msg>'), style=style)
        
        if not no_git:
            sp.text = 'Adding git repo...'
            add_git(target_dir)
            with sp.hidden():
                print(HTML(u'✅   <yay-msg>Git repo added</yay-msg>'), style=style)
        if not no_venv:
            sp.text = 'Creating virtual environment...'
            venv_path = os.path.join(target_dir, "venv")
            create_venv(venv_path)
            with sp.hidden():
                print(HTML(u'✅   <yay-msg>Virtual environment created</yay-msg>'), style=style)

            if not no_install:
                sp.text = 'Installing Python packages...'
                # click.echo('📦 Downloading packages...')
                req_path = os.path.join(target_dir, "requirements.txt")
                output = install_venv(req_path, venv_path)

                # remove lines starting with [notice]
                output = "\n".join([line for line in output.split("\n") if not line.startswith("[notice]")])

                with sp.hidden():
                    if len(output.strip()) > 0:
                        print(output)
                        print(HTML(u'❌   <err-msg>Oops...</err-msg>'), style=style)
                        exit(1)
                        
                    print(HTML(u'✅   <yay-msg>Python packages installed</yay-msg>'), style=style)

        click.echo('\n\n🍌 Project ready to go (hurrah!)')
        click.echo('\n\n🔥 To run a dev server locally:\n')
        
        if target_dir != ".":
            click.echo(f'cd {target_dir}')
        
        if no_install:
            click.echo(f'banana install')
        else:
            click.echo(f'source venv/bin/activate')
        
        click.echo('python3 app.py')

        click.echo('\n\n🚀 To call the model:\n')
        click.echo('python3 example.py\n\n')

@click.command()
@click.option('--venv', default="venv", required=False, type=str, help="The path of the virtual environment to install into. Defaults to venv.")
def install(venv):
    with yaspin(__spinner) as sp:
        if not os.path.exists(venv):
            sp.text = 'Creating virtual environment...'
            create_venv(venv)
            with sp.hidden():
                print(HTML(u'✅   <yay-msg>Virtual environment created</yay-msg>'), style=style)

        sp.text = 'Installing Python packages...'
        output = install_venv("requirements.txt", venv)

        # remove lines starting with [notice]
        output = "\n".join([line for line in output.split("\n") if not line.startswith("[notice]")])

        with sp.hidden():
            if len(output.strip()) > 0:
                print(output)
                print(HTML(u'❌   <err-msg>Oops...</err-msg>'), style=style)
                exit(1)
                
            print(HTML(u'✅   <yay-msg>Python packages installed</yay-msg>'), style=style)
        install_venv("requirements.txt", venv)

@click.command()
def deploy():
    with yaspin(__spinner) as sp:
        sp.text = 'Deploying model...'

        # download to rickroll.mp4
        url = "https://bananaml-model-files.s3.us-west-1.amazonaws.com/rickroll.mp4"
        r = requests.get(url, allow_redirects=True)
        open('rickroll.mp4', 'wb').write(r.content)

        roll("rickroll.mp4")

cli.add_command(init)
cli.add_command(install)
cli.add_command(deploy)

if __name__ == "__main__":
    cli()
