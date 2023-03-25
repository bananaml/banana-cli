# banana-cli

The goal of the Banana CLI is to bring an npm-like experience to ML development loops. 

This version includes:
- `banana init` to create a project with boilerplate
- `banana install` to install packages from the requirements.txt
- `banana dev` to run a dev server with hot-reload

[Here's a demo video](https://www.loom.com/share/86d4e7b0801549b9ab2f7a1acce772aa)

---
This is a v0 release using SemVer; it is not stable and the interface can break at any time.
---

## To use it

1. Install the CLI with pip
```bash
pip3 install banana-cli==0.0.10
```

2. Create a new project directory with 
```bash
banana init my-app
cd my-app
```
3. Start the dev server
```bash
banana dev
```

4. Call your API (from a separate terminal)
```bash
curl -X POST -H "Content-Type: application/json" -d '{"prompt": "Hello I am a [MASK] model."}' http://localhost:8000/
``` 

## Hot-Reload Dev Server

The interactive dev server works like a react, next, or nodemon server: it selectively hot reloads components when you save changes to different parts of your `app.py` file.

The init() function is ran on startup and for every change to init().

The handler() function is ran on every change to handler(), without needing to wait for a long init()

## Play with it:

4. Try changing the handler, see what happens!
5. Try changing the init, see what happens!

## Experimental features:
- `banana dev --auto-compat=True` to make your GPU code compatible with a CPU machine, by ignoring to("cuda") calls

## Future Development:
- Lock in a stable interface
- Add the following commands
  - `banana build` -> verify production build
  - `banana test` -> unit test against local test cases
  - `banana deploy` -> manually deploy from CLI
  - `banana deploy --canary --ttl=10` -> run a temporary deployment to Banana's cluster for on-GPU testin
- Port to Rust. [Why Rust?](https://giphy.com/gifs/aFbTasXn1GINgiEbzr)
