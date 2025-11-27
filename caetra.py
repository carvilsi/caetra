#!/usr/bin/env python3

import threading
import subprocess
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "./src/utils/"))
sys.path.append(os.path.join(os.path.dirname(__file__), "./src/"))

from logger_setup import logger
from config_parser import config
import constants


def run_script(script_name):
    subprocess.run(["python3", script_name])


# Threading execute all the shields under shield directory
def threading_excute_shields():
    shields = []
    shields_name = []
    for root, dirs, files in os.walk(constants.SHIELD_PATH):
        for file in files:
            if (
                file.endswith(".py")
                and file != constants.SHIELD_DEPLOYING_SCRIPT
                ):
                shieldname = os.path.splitext(file)[0]
                if config["caetra"].get("shields_enabled") is not None: 
                    if os.path.splitext(file)[0] in config["caetra"].get("shields_enabled"):
                        shields.append(os.path.join(root, file))
                        shields_name.append(shieldname)
                else:
                    shields.append(os.path.join(root, file))
                    shields_name.append(shieldname)
    logger.info(f"Deploying {len(shields)} Shields: \n\t\t\t\t\t{"\n\t\t\t\t\t".join(shields_name).upper()}\n")
    for shield in shields: 
        threading.Thread(target=run_script, args=(shield,)).start()


def main():
    logger.info("        ▗     ")
    logger.info("  ▛▘▀▌█▌▜▘▛▘▀▌")
    logger.info("  ▙▖█▌▙▖▐▖▌ █▌")
    logger.info("with <3 by (#4|2 \n\n")

    threading_excute_shields()


if __name__ == "__main__":
    main()
