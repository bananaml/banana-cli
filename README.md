# banana-cli
v0; work in progress; not stable release

The goal of the Banana CLI is to bring an npm-like experience to ML development loops. 
This version includes:
- `banana init` to create a project with boilerplate
- `banana dev` to run a dev server with hot-reload when app.py changes

---

## To use it

1. Install the CLI with pip
```bash
pip3 install banana-cli==0.0.6
```

2. Create a new project directory with 
```bash
banana init my-app
cd my-app
```
3. Start the hot reloading dev server
```bash
banana dev
```
The dev server expects you to already have jupyter notebook installed, runnable with `jupyter notebook`

## Hot-Reload Dev Server

The interactive dev server works like a react, next, or nodemon server: it selectively hot reloads components when you save changes to different parts of your `app.py` file.

The init() function is ran on startup and for every change to init().

The handler() function is ran on every change to handler(), without needing to wait for a long init()

It does this by pushing code in logical chunks to a jupyter notebook backend, to persist memory between reloads.

## Play with it:

6. Try changing the handler, see what happens!
7. Try changing the init, see what happens!