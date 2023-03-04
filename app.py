from transformers import pipeline
import torch
import time

cache = {}

def init():
    print("Init...")
    device = 0 if torch.cuda.is_available() else -1
    model = pipeline('fill-mask', model='bert-base-uncased', device=device)

    global cache
    cache = {
        "model": model
    }
    print("Done")

def handler() -> dict:
    print("Handler...")
    prompt = "What do you think about [MASK]"
    model = cache.get("model")
    outputs = model(prompt)
    print(outputs)


if __name__ == "__main__":
    init()
    handler()