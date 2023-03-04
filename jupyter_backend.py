import json
import requests
import datetime
import uuid
from websocket import create_connection

def create_client(token: str):
    # The token is written on stdout when you start the notebook
    base = 'http://localhost:8888'
    headers = {'Authorization': 'Token '+token}

    url = base + '/api/kernels'
    response = requests.post(url,headers=headers)
    kernel = json.loads(response.text)

    # Execution request/reply is done on websockets channels
    ws = create_connection("ws://localhost:8888/api/kernels/"+kernel["id"]+"/channels",
        header=headers)
    
    return ws

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
    ws = create_client("28a45e9ce6288759107020ff7ede2f2a7d4f2320ccc0504f")

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
