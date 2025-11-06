#!/usr/bin/env python

import threading
import subprocess
import os
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), './caetra_src/utils'))

from logger_setup import logger
from config_parser import config

SHIELD_PATH="./caetra_src/shields/"

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
    logger.info("        ▗     ") 
    logger.info("  ▛▘▀▌█▌▜▘▛▘▀▌")
    logger.info("  ▙▖█▌▙▖▐▖▌ █▌")
    logger.info("with <3 by (#4|2 \n\nDeploying Shields:\n") 

    print(config)

    threading_excute_shields()


    
if __name__ == "__main__":
    main()
