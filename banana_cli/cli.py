import click
import os
import requests
import json
import time

# local imports
from .cmd_dev import run_dev_server
from .utils import get_target_dir, get_app_path, get_site_packages, download_boilerplate, add_git, create_venv, install_venv
from .rick import roll
from .api import create_project, upload_project, build_project
from .server import start_server

# ui-related imports
from yaspin import yaspin, Spinner
from prompt_toolkit import HTML, print_formatted_text
from prompt_toolkit.styles import Style

# override print with feature-rich ``print_formatted_text`` from prompt_toolkit
print = print_formatted_text

# build a basic prompt_toolkit style for styling the HTML wrapped text
style = Style.from_dict({
    'msg': '#4caf50 bold',
    'yay-msg': '#7dff2b italic',
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

        click.echo('\n\n🚀 To call the project:\n')
        click.echo('pip3 install banana-dev')
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
def auth():
    # See comment below when calling __authenticate()
    __authenticate()

def __authenticate():
    called = False
    def auth_callback(data):
        nonlocal called
        called = True

        home_dir = os.path.expanduser("~")
        config_file = os.path.join(home_dir, ".banana", "config.json")
        if not os.path.exists(config_file):
            os.makedirs(os.path.dirname(config_file), exist_ok=True)
            with open(config_file, 'w') as f:
                json.dump({}, f, indent=4)
        with open(config_file) as f:
            config = json.load(f)
            if config.get("auth") is None:
                config["auth"] = {}
            config["auth"][data.get("teamID")] = {
                "apiKey": data.get("apiKey"),
                "teamName": data.get("teamName")
            }
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=4)

    auth_server, auth_server_port = start_server(auth_callback=auth_callback)

    app_url = "https://app.banana.dev"
    url = f"{app_url}/auth/cli?callback=http://localhost:{auth_server_port}/auth"
    
    click.echo(f"🖥️    Authenticating in the web app\n\n")

    with yaspin(__spinner) as sp:
        sp.text = 'Waiting for token...'

        import webbrowser
        webbrowser.open(url)

        while not called:
            time.sleep(1)

        auth_server.stop()

        with sp.hidden():
            print(HTML(u'✅   <yay-msg>Authenticated</yay-msg>'), style=style)

@click.command()
def deploy():
    with yaspin(__spinner) as sp:

        # does the current directory have a .banana/config.json?
        # does it have a model id? if so, deploy to that model id
        # if not, present selection of teams from ~/.banana/config
        # if ~/.banana/config not configured, authenticate with web app
        # add team id to the folder's .banana/config.json
        # call the create_project() function and save the resulting model id in the folder's .banana/config.json

        config = {}
        api_key = None

        def configure_team():
            home_dir = os.path.expanduser("~")
            global_config_file = os.path.join(home_dir, ".banana", "config.json")
            if os.path.exists(global_config_file):
                with open(global_config_file) as f:
                    with sp.hidden():
                        global_config = json.load(f)
                        teams = global_config.get("auth", {})
                        # team keys to array
                        keys = list(teams.keys())

                        if len(keys) > 1:
                            for idx, team_id in enumerate(keys):
                                click.echo(f"{str(idx+1)}: {teams.get(team_id).get('teamName', team_id)}")

                            # Add team id to the folder's .banana/config.json
                            selected_team_idx = click.prompt("Which team do you want to use: ", type=int)
                            selected_team_id = keys[selected_team_idx-1]
                        else:
                            # If there's only one team, just select it.
                            selected_team_id = keys[0]

                        config["teamId"] = selected_team_id
                        api_key = teams.get(selected_team_id).get("apiKey")
                        with open(config_file, 'w') as f:
                            json.dump(config, f, indent=4)

                        click.echo("\n\n")
            else:
                # needs to call an internal function rather than a click command?
                __authenticate()
                configure_team()

        def get_api_key(team_id):
            home_dir = os.path.expanduser("~")
            global_config_file = os.path.join(home_dir, ".banana", "config.json")
            if os.path.exists(global_config_file):
                with open(global_config_file) as f:
                    global_config = json.load(f)
                    teams = global_config.get("auth", {})
                    return teams.get(team_id).get("apiKey")
            
            # todo: error case
            return None

        # Check if the current directory has a .banana/config.json
        config_dir = os.path.join(os.getcwd(), ".banana")
        config_file = os.path.join(config_dir, "config.json")

        if not os.path.exists(config_dir):
            os.makedirs(config_dir)

        if not os.path.exists(config_file):
            # If not, create one
            with open(config_file, 'w') as f:
                f.write("")

        with open(config_file) as f:
            str_contents = f.read()
            if len(str_contents.strip()) == 0:
                config = {}
            else:
                try:
                    config = json.loads(str_contents)
                except:
                    config = None

        if config is None:
            with sp.hidden():
                print(HTML(u'❌   <err-msg>Error parsing .banana/config.json</err-msg>'), style=style)
                exit(1)

        if "teamId" not in config:
            # set team id in local config
            configure_team()

        if "projectId" not in config:
            # If teamId exists and projectId doesn't, proceed with project creation
            # get the apiKey from ~/.banana/config {"auth":{"<teamId>":{"apiKey":"<apiKey>"}}}
            sp.text = 'Creating new project...'
            with sp.hidden():
                api_key = get_api_key(config.get("teamId"))

                # get the folder name from the current directory
                folder = os.getcwd().split("/")[-1]
                result = create_project(api_key, folder)

                # set project id in local config
                config["projectId"] = result.get("id")
                with open(config_file, 'w') as f:
                    json.dump(config, f, indent=4)

                print(HTML(u'✅   <yay-msg>Project created</yay-msg>'), style=style)
        else:
            api_key = get_api_key(config.get("teamId"))

        # todo: the model exists and re-deploying case

        sp.text = 'Deploying project...'
        
        upload_response = upload_project(api_key, config.get("projectId"))
        if upload_response is None:
            with sp.hidden():
                print(HTML(u'❌   <err-msg>Error getting upload URL for project</err-msg>'), style=style)
                exit(1)
        upload_url = upload_response.get("uploadUrl")
        upload_key = upload_response.get("key")

        import tarfile
        from gitignore_parser import parse_gitignore

        matches = parse_gitignore('.gitignore')

        filename = "archive.tar.gz"

        sp.text = 'Archiving folder contents...'

        # Archive the current folder
        with tarfile.open(filename, "w:gz") as tar:
            for root, dirs, files in os.walk('.'):
                # Ignore .venv and venv folders
                dirs[:] = [d for d in dirs if d not in ['.venv', 'venv', '.git', '.banana'] and not matches(d)]
                for file in files:
                    if not matches(file) and file != "rickroll.mp4" and file != ".DS_Store":
                        file_path = os.path.join(root, file)
                        # Use the relative path from the current directory
                        relative_path = os.path.relpath(file_path, '.')
                        tar.add(file_path, arcname=relative_path)

        with sp.hidden():
            print(HTML(u'✅   <yay-msg>Archived</yay-msg>'), style=style)

        sp.text = 'Uploading...'

        def upload_to_presigned_url(presigned_url, file_path):
            with open(file_path, 'rb') as f:
                data = f.read()
                response = requests.put(presigned_url, data=data)
            return response
        
        response = upload_to_presigned_url(upload_url, filename)
        os.remove(filename)

        # todo
        if response.status_code != 200:
            with sp.hidden():
                print(HTML(u'❌   <err-msg>Error uploading project code</err-msg>'), style=style)
                return
            
        with sp.hidden():
            print(HTML(u'✅   <yay-msg>Uploaded</yay-msg>'), style=style)

        sp.text = 'Triggering build...'

        build_project_response = build_project(api_key, config.get("projectId"), upload_key)

        with sp.hidden():
            print(HTML(u'✅   <yay-msg>Build triggered</yay-msg>'), style=style)

        sp.text = ""

    click.echo("\n\n⏳ To view build logs and deployment progress, go to:")
    click.echo(f"\n🔗 https://app.banana.dev/project/{config.get('projectId')}\n")  


@click.command()
def stage():
    """Experimental feature: staging deploy. Not yet implemented. But give it a try anyway."""
    
    with yaspin(__spinner) as sp:
        sp.text = 'Creating staging deploy...'
        time.sleep(3)

    # download to rickroll.mp4
    url = "https://bananaml-model-files.s3.us-west-1.amazonaws.com/rickroll.mp4"
    r = requests.get(url, allow_redirects=True)
    open('rickroll.mp4', 'wb').write(r.content)

    roll("rickroll.mp4")

cli.add_command(init)
cli.add_command(install)
cli.add_command(auth)
cli.add_command(deploy)
cli.add_command(stage)

if __name__ == "__main__":
    cli()
