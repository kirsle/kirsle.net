#!/usr/bin/env python3

"""Bootstrap script to set up a local dev instance of Kirsle.net

This will `git clone` an instance of the Rophako CMS and configure it to run
this local website. When the dev Rophako instance already exists, running this
script again acts as a shortcut to running `python runserver.py` from within
the Rophako git repo.

This script is only designed to work in Python 3 and requires the `git` and
`pyvenv` commands.

This performs the following tasks:
* Clones Rophako into ./rophako
* Sets up a Python 3 virtual environment via `pyvenv` at ./rophako/pyvenv
* Installs requirements via `pip` into its virtual environment
* Symlinks settings.yml and kirsle_legacy.py into the Rophako root
* Runs the server
"""

import os
import os.path
import subprocess
import sys

def main():
    # Make sure we have everything we need.
    check_depends()

    # Do we already have Rophako?
    if os.path.isdir("./rophako"):
        os.chdir("./rophako")
    else:
        # Clone it.
        must_run(["git", "clone", "https://github.com/kirsle/rophako"])
        os.chdir("./rophako")

        # Make the Python environment.
        must_run(["pyvenv", "pyvenv"])
        must_run(["pyvenv/bin/pip", "install", "-r", "requirements.txt"])

        # Configure it.
        os.symlink("../settings.yml", "settings.yml")
        os.symlink("../kirsle_legacy.py", "kirsle_legacy.py")

        print("=" * 80)
        print("Success! Rophako has been cloned and configured! The server")
        print("will now start. To quickly start the server again in the")
        print("future, just run bootstrap.py again.")
        print("=" * 80)

    # Run Rophako.
    must_run(["pyvenv/bin/python", "runserver.py"])

def check_depends():
    # Make sure we have access to required commands.
    errors = False
    for command in [ "git", "pyvenv" ]:
        try:
            subprocess.check_call(["which", command],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except subprocess.CalledProcessError:
            print("You seem to be missing the command: {}".format(command))
            errors = True

    if errors:
        print("Make sure the required commands are installed and try again.")
        sys.exit(1)

def must_run(args, **kwargs):
    """Calls subprocess to run a command which must succeed or die."""
    result = subprocess.call(args, **kwargs)
    if result != 0:
        print("Errors were detected in the command I tried to run: {}".format(
            " ".join(args),
        ))
        sys.exit(1)

if __name__ == "__main__":
    main()
