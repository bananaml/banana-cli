import json
import requests
import datetime
import uuid
import re
import signal, atexit
import subprocess
import time
from termcolor import colored
from websocket import create_connection

# Graceful shutdown, to prevent memory leaking a bunch of jupyter kernal procesees onto the users machine,
jupyter_proc = None
already_handled = False # because handle_exit can double-fire
def handle_exit(*args):
    global already_handled
    if already_handled:
        quit()
    already_handled=True
    global jupyter_proc
    if jupyter_proc == None:
        quit()
    print(colored("\n\nCleaning up...", 'green'))
    jupyter_proc.kill()
    print("Done")
    quit()
atexit.register(handle_exit)
signal.signal(signal.SIGTERM, handle_exit)
signal.signal(signal.SIGINT, handle_exit)

# Runs `jupyter notebook` as a background subprocess, and handles any errors in that
def start_jupyter():
    bashCommand = "jupyter notebook --no-browser"
    try:
        # run as subprocess. Jupyter funnels output into both stdout and stderr for some reason so we pipe them both to process.stdout
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except FileNotFoundError:
        print("Jupyter Notebook not found in your environment.\n\nSee https://jupyter.org/install for installation instructions\nAfter installation, be sure it's runnable with `jupyter notebook`")
        quit()
    
    log_dump = ""
    port = None
    token = None
    # startup should take less than a second so capture start time for timeout error
    start = time.time()

    for line in process.stdout:
        # if we're still reading from stdout after 10s, that's unexpected
        if time.time() - start > 10:
            raise Exception("Error: timed out starting jupyter subprocess. Make sure you have jupyter installed, and that it's runnable with `jupyter notebook`")
        
        line = line.decode()
        # add line into log_dump in case errors arise
        log_dump += line

        # search for the server url
        x = re.search("http://localhost:", line)
        if x == None:
            # keep reading from stream if we haven't seen a server url
            continue
        # parse out port and token
        port_parse_start = x.string.find("http://localhost:") + 17
        port_parse_end = x.string.find("/?token=")
        port = x.string[port_parse_start:port_parse_end].strip()
        token_parse_start = port_parse_end + 8
        token = x.string[token_parse_start:].strip()
        break

    # if we hit EOF without recognizing a port or token, that means an error occured
    if port == None or token == None:
        print(f"Error: running {bashCommand}, here's a log dump")
        print(colored(log_dump, "red"))
        raise Exception("Error in starting jupyter subprocess, view logs above")
    
    # save that process to the global var for graceful shutdown
    global jupyter_proc
    jupyter_proc = process

    return port, token

# create a websocket client connection to the juptyer backend
def create_client(port: str, token: str):
    base = f'http://localhost:{port}'
    headers = {'Authorization': 'Token '+token}
    url = base + '/api/kernels'
    response = requests.post(url,headers=headers)
    kernel = json.loads(response.text)

    # Execution request/reply is done on websockets channels
    ws = create_connection(f"ws://localhost:{port}/api/kernels/"+kernel["id"]+"/channels",
        header=headers)
    
    return ws

# creates the expected request structure to the jupyter backend
def form_request(code: str):
    msg_type = 'execute_request'
    content = { 'code' : code, 'silent':False }
    hdr = { 'msg_id' : uuid.uuid1().hex, 
        'username': 'test', 
        'session': uuid.uuid1().hex, 
        'data': datetime.datetime.now().isoformat(),
        'msg_type': msg_type,
        'version' : '5.0' }
    msg = { 'header': hdr, 'parent_header': hdr, 
        'metadata': {},
        'content': content }
    return json.dumps(msg)

# Excecutes arbitrary code as a single jupyter cell in the jupter backend
def run_code(ws, code: str):
    ws.send(form_request(code))

    # We ignore all the other messages, we just get the code execution output
    # (this needs to be improved for production to take into account errors, large cell output, images, etc.)
    msg_type = ''
    while True:
        rsp = json.loads(ws.recv())
        msg_type = rsp["msg_type"]

        # display errors if any
        if msg_type == "error":
            for line in rsp["content"]["traceback"]:
                print(line)
            break

        # display stdout if any
        if "content" in rsp:
            if "name" in rsp["content"]:
                if rsp["content"]["name"] == "stdout":
                    print(rsp["content"]["text"], end="")
  
        if msg_type == "execute_reply":
            break
  

# Run this file directly for testing
if __name__ == "__main__":

    port, token = start_jupyter()
    
    ws = create_client(port, token)

    print("Case 1")
    to_run = '''
import time

print("start of sleep")
time.sleep(5)
print("end of sleep")
    '''

    run_code(ws, to_run)

    print("Case 2")
    to_run = '''
import time
a = 1/0
    '''

    run_code(ws, to_run)
