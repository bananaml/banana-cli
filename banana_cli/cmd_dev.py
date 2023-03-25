import time
from termcolor import colored
import os
# from .jupyter_backend import create_client, run_code, start_jupyter
from .process.run import run_cell, check_for_gpu
from .process import cells

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

replacements = {}
# populate_replacements gathers all patterns seen for CUDA usage in pytorch and provides a replacement value for use in str.replace()
def populate_replacements():
    replacements = {
        ".cuda()": "", 
        "device='cuda'": "device='cpu'",
        "device = 'cuda'": "device = 'cpu'",
        'device="cuda"': 'device="cpu"',
        'device = "cuda"': 'device = "cpu"'
    }

    slots = [""] # the all gpus slot
    # we only support for up to 8 GPUs, and do not support specific numbered gpus such as `cuda:1,3`
    for i in range(8):
        slots.append(f":{i}")

    # add named slots
    for slot in slots:
        replacements[f".to('cuda{slot}')"] = ""
        replacements[f'.to("cuda{slot}")'] = ""

        # devices that may be later referenced
        replacements[f"torch.device('cuda{slot}')"] = "torch.device('cpu')"
        replacements[f'torch.device("cuda{slot}")'] = "torch.device('cpu')"

    # device indices
    for i in range(8):
        replacements[f"device={i}"] = "device=-1"
        replacements[f"device = {i}"] = "device = -1"

    return replacements

# strip_cuda_calls replaces calls to cuda with calls to cpu
def strip_cuda_calls(block: str):
    # from https://pytorch.org/docs/stable/notes/cuda.html

    global replacements
    if len(replacements) == 0:
        # populate it
        replacements = populate_replacements()

    
    old_block = block
    changed = False
    for substr, new in replacements.items():
        block = block.replace(substr, new)
    if block != old_block:
        changed = True

    return block, changed

def start_all(b1, b2, first_run = False):
    if first_run:
        print(colored("------\nStarting server 🍌", 'yellow'))
    else:
        print(colored("------\nRestarting server 🍌", 'yellow'))
    # define init and handlers
    run_cell(b1)
    run_cell(b2)
    # run init
    print(colored("Running init()", 'yellow'))
    run_cell(cells.run_init)
    # start server
    run_cell(cells.start_server)
    print(colored("Serving on http://localhost:8000\n------", 'green'))

def reload_all(b1, b2):
    # stop server then restart
    run_cell(cells.stop_server)
    start_all(b1, b2)
             
def reload_handlers(b2):
    print(colored("------\nHot reloading 🔥", 'yellow'))
    # stop server
    run_cell(cells.stop_server)
     # redefine handlers
    run_cell(b2)
    # start server
    run_cell(cells.start_server)
    print(colored("Reloaded\n------", 'green'))

# runs a hot-reload dev server
def run_dev_server(app_path, site_packages, auto_compat):
    import signal
    import sys
    # shut down thread if one is runnning
    def sigint_handler(signal, frame):
        print(colored("\nStopping server", 'yellow'))
        run_cell(cells.stop_server_quietly)
        print(colored("Bye! 👋\n------", 'green'))
        sys.exit(0)
    signal.signal(signal.SIGINT, sigint_handler)

    # DISCLAIMER: this script:
    # - assumes handler is all code after init block
    # - does not detect changes in imported files
    # - probably has a bunch of bugs

    # run session backend in virtualenv, or in global env if venv not found
    if site_packages != None:
        run_cell("import sys")
        run_cell(f"sys.path.append('{site_packages}')")
    else:
        print(colored("Warning: no virtual environment found; running in global environment", 'yellow'))

    if auto_compat:
        gpu_exists = check_for_gpu()
    compat_warning_raised = False # for a one-time warning

    # imports and classes needed for hot reload serving
    run_cell(cells.prepare_env)

    prev_b1 = 0
    prev_b2 = 0
    first_run = True
    while True:
        b1, b2 = split_file(app_path)
        
        if auto_compat and not gpu_exists:
            b1, changed_b1 = strip_cuda_calls(b1)
            b2, changed_b2 = strip_cuda_calls(b2)
            if (changed_b1 or changed_b2) and not compat_warning_raised:
                print(colored("Auto-compat warning: GPU calls have been replaced with CPU calls", 'yellow'))
                compat_warning_raised = True
                
        
        if first_run:
            start_all(b1, b2, first_run)
            first_run = False
            prev_b1 = b1
            prev_b2 = b2
            continue

        if b1 != prev_b1:
            reload_all(b1, b2)
            prev_b1 = b1
            prev_b2 = b2
            continue

        if b2 != prev_b2:
            reload_handlers(b2)
            prev_b2 = b2
        
        time.sleep(0.1)