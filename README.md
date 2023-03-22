# banana-cli

The goal of the Banana CLI is to bring an npm-like experience to ML development loops. 

This version includes:
- `banana init` to create a project with boilerplate
- `banana install` to install packages from the requirements.txt
- `banana dev` to run a dev server with hot-reload

It's currently written in Python, we plan to port to Rust for stable release. [Why Rust?](https://giphy.com/gifs/aFbTasXn1GINgiEbzr)

---

## To use it

1. Install the CLI with pip
```bash
pip3 install banana-cli==0.0.7
```

2. Create a new project directory with 
```bash
banana init my-app
cd my-app
```
1. Start the dev server
```bash
banana dev
```

## Hot-Reload Dev Server

The interactive dev server works like a react, next, or nodemon server: it selectively hot reloads components when you save changes to different parts of your `app.py` file.

The init() function is ran on startup and for every change to init().

The handler() function is ran on every change to handler(), without needing to wait for a long init()

## Play with it:

6. Try changing the handler, see what happens!
7. Try changing the init, see what happens!
