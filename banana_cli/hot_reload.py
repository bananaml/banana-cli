import time
from termcolor import colored
from .jupyter_backend import create_client, run_code

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

def run_dev_server(watchfile):


    # DISCLAIMER: this script:
    # - assumes handler is all code after init block
    # - does not detect changes in imported files
    # - probably has a bunch of bugs

    # Run `juptyer notebook` in this venv, and copy the token string from the URL it gives you
    print("The Banana CLI uses jupyter on the backend to execute hot-reloading.")
    print("For this V0, you need to start that server yourself.\n")
    print("In a separate terminal session:")
    print("1. cd into this repo")
    print("2. create a python virtual env with `python3 -m venv venv`")
    print("3. activate into that env with `. ./venv/bin/activate`")
    print("4. install dependencies with `pip3 install -r requirements.txt`")
    print("5. run a jupyter notebook backend with `jupyter notebook`. Install if needed.")
    print("6. copy the auth token from the juptyer notebook terminal output, from the ?token=xyz field in the URLs. Paste it below:\n")
    jupyter_token = input("Your jupyter token: ")

    ws = create_client(jupyter_token)

    prev_b1 = 0
    prev_b2 = 0
    while True:
        b1, b2 = split_file(watchfile)
        if b1 != prev_b1:
            print(colored("\n------\ninit block changed\nrestarting init + handler\n------", 'green'))
            prev_b1 = b1
            prev_b2 = b2

            print(colored("init output:", 'yellow'))
            to_run = b1 + "\ninit()"
            run_code(ws, to_run)

            print(colored("handler output:", 'yellow'))
            to_run = b2 + "\nhandler()"
            run_code(ws, to_run)
            continue

        if b2 != prev_b2:
            print(colored("\n------\nhandler block changed\nupdating handler\n------", 'green'))
            prev_b2 = b2

            print(colored("handler output:", 'yellow'))
            to_run = b2 + "\nhandler()"
            run_code(ws, to_run)
        
        time.sleep(0.1)