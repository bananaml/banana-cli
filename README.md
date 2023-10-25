# banana-cli

The goal of the Banana CLI is to bring an npm-like experience to ML development loops. 

This version includes:
- `banana init` to create a project with boilerplate
- `banana install` to install packages from the requirements.txt
- `banana --version` to show the current version
- `banana deploy` to easily deploy the local folder to Banana.dev without using GitHub

[Here's a demo video](https://www.loom.com/share/86d4e7b0801549b9ab2f7a1acce772aa)


## Installing the CLI locally

```
python3 -m venv .venv
source .venv/bin/activate
pip3 install -e ./
banana --version
```

---
This is a v0 release using SemVer; it is not stable and the interface can break at any time.
---

## To use it

1. Create a new project directory with 
```bash
banana init my-app
cd my-app
```
2. Start the dev server
```bash
python3 app.py
```

3. Call your API (from a separate terminal)
```bash
curl -X POST -H "Content-Type: application/json" -d '{"prompt": "Hello I am a [MASK] model."}' http://localhost:8000/
``` 

The interactive dev server works like a react, next, or nodemon server: it selectively hot reloads components when you save changes to different parts of your `app.py` file.

The init() function is ran on startup and for every change to init().

The handler() function is ran on every change to handler(), without needing to wait for a long init()

## Play with it:

4. Try changing the handler, see what happens!
5. Try changing the init, see what happens!

## Future Development:
- Lock in a stable interface
- Add the following commands
  - `banana stage` -> run a temporary deployment to Banana's cluster for on-GPU testing
  - `banana test` -> unit test against local test cases
