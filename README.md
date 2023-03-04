# banana-cli (WORK IN PROGRESS)

The Banana CLI helps you build Potassium apps

## Hot-Reload Dev Server

The interactive dev server works like a react, next, or nodemon server in that it hot reloads on changes to different parts of your `app.py` file.

On startup, and on changes to the init() block, it runs init() and handler().

On changes to the handler() block, it reruns the handler() without needing to wait for another init

It does this by pushing code in logical chunks to a jupyter notebook backend, to persist memory between refreshes.

### To use it

Start the jupyter backend:
1. set up a virtual env `python3 -m venv venv`
2. activate into that env `. ./venv/bin/activate`
3. install dependencies `pip3 install -r requirements.txt`
4. run a jupyter notebook server `jupyter notebook`
   - Copy the "token" string in the URL
   
Run the code watcher:
(in a new shell)
5. Put that token into watcher.py as jupyter_token
6. Run watcher.py `python3 watcher.py` to watch app.py for changes

Play with it:
7. Try changing the handler, see what happens!
8. Try changing the init, see what happens!
