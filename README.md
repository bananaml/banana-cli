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
pip3 install banana-cli==0.0.4
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

For the current release you'll need to manually start a jupyter notebook backend. The `banana dev` command will prompt you to input the auth token from that backend so the CLI can connect to it. This will be automatic in the future.

4. Start the jupyter backend (in a separate terminal session):

From within your `my-app` project directory:
```bash
python3 -m venv venv
. ./venv/bin/activate
pip3 install -r requirements.txt
jupyter notebook
```
5. Copy the "token" string in the URL displayed in the terminal output. It should look like `115850cc76a1dd8b2880ccfa458f6f4d269876724eef92bc` 

## Hot-Reload Dev Server

The interactive dev server works like a react, next, or nodemon server: it selectively hot reloads components when you save changes to different parts of your `app.py` file.

The init() function is ran on startup and for every change to init().

The handler() function is ran on every change to handler(), without needing to wait for a long init()

It does this by pushing code in logical chunks to a jupyter notebook backend, to persist memory between reloads.

   
## Play with it:

6. Try changing the handler, see what happens!
7. Try changing the init, see what happens!