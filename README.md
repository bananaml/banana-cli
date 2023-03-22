# banana-cli

The goal of the Banana CLI is to bring an npm-like experience to ML development loops. 

This version includes:
- `banana init` to create a project with boilerplate
- `banana install` to install packages from the requirements.txt
- `banana dev` to run a dev server with hot-reload

---
This is a v0 release using SemVer; it is not stable and the interface can break at any time.
---

## To use it

1. Install the CLI with pip
```bash
pip3 install banana-cli==0.0.8
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

## Hot-Reload Dev Server

The interactive dev server works like a react, next, or nodemon server: it selectively hot reloads components when you save changes to different parts of your `app.py` file.

The init() function is ran on startup and for every change to init().

The handler() function is ran on every change to handler(), without needing to wait for a long init()

## Play with it:

4. Try changing the handler, see what happens!
5. Try changing the init, see what happens!

## Future Development:
- Rewrite boilerplate and dev server to run [Potassium](https://github.com/bananaml/potassium) rather than the current demo code
- Lock in a stable interface
- Add the following commands
  - `banana build` -> verify production build
  - `banana test` -> unit test against local test cases
  - `banana deploy` -> manually deploy from CLI
  - `banana deploy --canary --ttl=10` -> run a temporary deployment to Banana's cluster for on-GPU testin
- Port to Rust. [Why Rust?](https://giphy.com/gifs/aFbTasXn1GINgiEbzr)
