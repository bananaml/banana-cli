import os
import venv
import shutil
import subprocess
import sys
import click

# Uses git to clone the potassium boilerplate from /boilerplate/potassium in this git repo
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

# Get the relative path to whatever directory the user specified
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

# Get the relative path to the users app.py (or equiv. named file)
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

# Get the relative path to the venv site-packages
# Return None if not exists
def get_site_packages(app_path, venv_name = "venv"):
    parent_dir = os.path.split(os.path.abspath(app_path))[0]
    venv_dir = os.path.join(parent_dir, venv_name)
    if not os.path.exists(venv_dir) or not os.path.isdir(venv_dir):
        return None

    # Drill in to site packages at /{venv}/lib/python{some version}/site-packages
    lib_path = os.path.join(venv_dir, "lib")
    if not os.path.exists(lib_path):
        return None
    python_versions = os.listdir(lib_path)
    # There should only be one python version. If more, there's some trickery afoot.
    if len(python_versions) != 1:
        return None
    site_packages_dir = os.path.relpath(os.path.join(lib_path, python_versions[0], "site-packages"))
    if not os.path.exists(site_packages_dir) or not os.path.isdir(site_packages_dir):
        return None 
    
    return site_packages_dir

# create a venv
def create_venv(venv_path):
    venv.create(venv_path, with_pip=True)

# install requirements.txt into venv
def install_venv(req_path, venv_path):
    python_interpreter = os.path.join(venv_path, "bin", "python3")
    subprocess.check_call([python_interpreter, "-m", "pip", "install", "-r", req_path])