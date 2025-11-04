#!/usr/bin/env python

import threading
import subprocess
import os

SHIELD_PATH="./shields/"

def run_script(script_name):
    subprocess.run(["python", script_name])


def threading_excute_shields():
    # Threading execute all the shields under shield directory
    for (root, dirs, files) in os.walk(SHIELD_PATH):
        for file in files:
            if file.endswith(".py") and file != "deploying.py":
                shield = os.path.join(root, file)
                threading.Thread(target=run_script, args=(shield,)).start()


def main():
    print("        ▗     ") 
    print("  ▛▘▀▌█▌▜▘▛▘▀▌")
    print("  ▙▖█▌▙▖▐▖▌ █▌")
    print("with <3 by (#4|2 \n\nDeploying Shields:\n") 

    threading_excute_shields()

    
if __name__ == "__main__":
    main()
