###
# NOTE: 
# This app.py is for demo purposes only. 
# Future versions of the CLI will use the Potassium framework, and actually run a callable http server
# This app.py simply prints test cases, for the sake of showing off the hot-reload.
###

from transformers import pipeline
import torch
import time

cache = {}

def init():
    print("Loading model...")
    device = 0 if torch.cuda.is_available() else -1
    model = pipeline('fill-mask', model='bert-base-uncased', device=device)

    time.sleep(1) # sleep to simulate a hefty model load

    global cache
    cache = {
        "model": model
    }
    print("Done")

def handler() -> dict:
    print("Running Model...")
    prompt = "The capital of California is [MASK]."
    model = cache.get("model")
    outputs = model(prompt)
    print(outputs)


if __name__ == "__main__":
    init()
    handler()