import time
from termcolor import colored
import os
# from .jupyter_backend import create_client, run_code, start_jupyter
from .process.run import run_cell

# splits a python file into an init section and a handler section
def split_file(watch):
     # split after init
    with open(watch, "r") as file:
        lines = file.readlines()
    in_init_block = False
    init_end = 0
    handler_end = 0
    for i, line in enumerate(lines):
        if "def init()" in line:
            in_init_block = True
            continue
        if 'if __name__ == "__main__":' in line:
            handler_end = i
        if in_init_block:
            # if that line is not empty, and not indented, the init block has finished
            if len(line)>0 and len(line) - len(line.lstrip()) == 0 :
                init_end = i
                in_init_block = False
                
    init_block_lines = lines[:init_end]
    handler_block_lines = lines[init_end:handler_end]

    # strip empty lines to avoid unnecessary rebuilds, then join to string
    init_block = "".join([line for line in init_block_lines if line != "\n"])
    handler_block = "".join([line for line in handler_block_lines if line != "\n"])

    return init_block, handler_block

# runs a hot-reload dev server
def run_dev_server(app_path, site_packages):

    # DISCLAIMER: this script:
    # - assumes handler is all code after init block
    # - does not detect changes in imported files
    # - probably has a bunch of bugs

    # run session backend in specified virtualenv
    run_cell("import sys")
    run_cell(f"sys.path.append('{site_packages}')")

    prev_b1 = 0
    prev_b2 = 0
    first_run = True
    while True:
        b1, b2 = split_file(app_path)
        if b1 != prev_b1:
            if first_run:
                print(colored("\n------\nStarting server 🍌\n------", 'green'))
                first_run = False
            else:
                print(colored("\n------\nInit block changed\nRestarting init + handler\n------", 'green'))
            prev_b1 = b1
            prev_b2 = b2

            print(colored("Init output:\n------", 'yellow'))
            to_run = b1 + "\ninit()"
            # run_code(ws, to_run)
            run_cell(to_run)

            print(colored("\nHandler output:\n------", 'yellow'))
            to_run = b2 + "\nhandler()"
            # run_code(ws, to_run)
            run_cell(to_run)
            continue

        if b2 != prev_b2:
            print(colored("\n------\nHandler block changed\nUpdating handler\n------", 'green'))
            prev_b2 = b2

            print(colored("Handler output:\n------", 'yellow'))
            to_run = b2 + "\nhandler()"
            # run_code(ws, to_run)
            run_cell(to_run)
        
        time.sleep(0.1)