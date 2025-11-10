#!/usr/bin/env python

import threading
import subprocess
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), './src/utils/'))
sys.path.append(os.path.join(os.path.dirname(__file__), './src/'))

from logger_setup import logger
import constants


def run_script(script_name):
    subprocess.run(["python", script_name])


# Threading execute all the shields under shield directory
def threading_excute_shields():
    for (root, dirs, files) in os.walk(constants.SHIELD_PATH):
        for file in files:
            if file.endswith(".py") and file != constants.SHIELD_DEPLOYING_SCRIPT:
                shield = os.path.join(root, file)
                threading.Thread(target=run_script, args=(shield,)).start()


def main():
    logger.info("        ▗     ") 
    logger.info("  ▛▘▀▌█▌▜▘▛▘▀▌")
    logger.info("  ▙▖█▌▙▖▐▖▌ █▌")
    logger.info("with <3 by (#4|2 \n\nDeploying Shields:\n") 

    threading_excute_shields()


    
if __name__ == "__main__":
    main()
