import requests
import os
import json

home_dir = os.path.expanduser("~")
config_file = os.path.join(home_dir, ".banana", "config.json")

ROOT_URL = "https://api.banana.dev/v1"

def create_project(api_key, name):
    url = ROOT_URL + "/projects"

    response = requests.post(url, json={"name": name}, headers={
        "X-Banana-API-Key": api_key,
    })

    if response.status_code == 200:
        return response.json()
    
    # todo
    return None

def upload_project(api_key, project_id):
    url = ROOT_URL + "/projects/" + project_id + "/upload"

    response = requests.post(url, json={}, headers={
        "X-Banana-API-Key": api_key,
    })

    if response.status_code == 200:
        return response.json()
    
    # todo
    return None

def build_project(api_key, project_id, key):
    url = ROOT_URL + "/projects/" + project_id + "/build"

    response = requests.post(url, json={
        "key": key
    }, headers={
        "X-Banana-API-Key": api_key,
    })

    if response.status_code == 200:
        return response.json()
    
    # todo
    return None
