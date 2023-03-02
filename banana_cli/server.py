import os, sys, time

def run_dev_server(app_path: str):
    # this is incredibly hacky
    # if you're reading this, I've warned you.

    # run this in their project venv
    # this currently assumes they have a single python version venv in this directory
    # it also assumes the python version (major+minor) for their potassium app is the same as the banana-cli version
    v = sys.version
    maj_min = v.split(".")[0:2]
    venv_python = "python"+".".join(maj_min)

    # add that venv to python import path
    sys.path.append(os.path.join(os.getcwd(), f"venv/lib/{venv_python}/site-packages"))

    # import that app and execute it
    import importlib.util
    spec = importlib.util.spec_from_file_location("module.name", app_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["module.name"] = module
    spec.loader.exec_module(module) # assumes there's an if __name__ == "__main__" clause that actually starts the server, so that our import here doesn't start any processes. We want to start it ourselves.
   
    # now we can do whatever we want from that

    app = module.app

    print("Starting server within CLI interpreter")
    app.serve()