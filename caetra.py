#!/usr/bin/env python3

import threading
import subprocess
import os
import sys

from src.utils.logger_setup import logger
from src.utils.config_parser import config
import src.constants as constants


def run_script(script_name):
    module = (
        script_name[2:-3].replace(os.sep, ".")
    )

    subprocess.run(["python3", "-m", module])


# Threading execute all the shields under shield directory
def threading_excute_shields():
    shields = []
    shields_name = []
    for root, dirs, files in os.walk(constants.SHIELD_PATH):
        for file in files:
            if (
                file.endswith(".py")
                and file != constants.SHIELD_DEPLOYING_SCRIPT
                and file != constants.SHIELD_STATUS_HANDLER_SCRIPT
            ):
                shieldname = os.path.splitext(file)[0]
                if config["caetra"].get("shields_enabled") is not None:
                    if os.path.splitext(file)[0] in config["caetra"].get(
                        "shields_enabled"
                    ):
                        shields.append(os.path.join(root, file))
                        shields_name.append(shieldname)
                else:
                    shields.append(os.path.join(root, file))
                    shields_name.append(shieldname)
    logger.info(
        f"Going to deploy {len(shields)} Shields: \n\t\t\t\t\t{'\n\t\t\t\t\t'.join(shields_name).upper()}\n"
    )
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
