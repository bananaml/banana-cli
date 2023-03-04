# banana-cli (WORK IN PROGRESS)

The Banana CLI helps you build Potassium apps

## Hot-Reload Dev Server

The interactive dev server works like a react, next, or nodemon server in that it hot reloads on changes to different parts of your `app.py` file.

On startup, and on changes to the init() block, it runs init() and handler().

On changes to the handler() block, it reruns the handler() without needing to wait for another init

It does this by pushing code as logical to a jupyter notebook backend.

### To use it

1. set up a virtual env `python3 -m venv venv`
2. activate into that env `. ./venv/bin/activate`
3. install dependencies `pip3 install -r requirements.txt`
4. run a jupyter notebook server `jupyter notebook`
   - Copy the "token" string in the URL
5. Put that token into watcher.py as jupyter_token
6. (with the jupyter server running in a separate shell) run watcher.py `python3 watcher.py`
