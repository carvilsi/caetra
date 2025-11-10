from bcc import BPF
from logger_setup import logger
import tomllib
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
import constants
from caetra_exceptions import ShieldConfigurationError


# returns a BPF program loaded and attached to kernel
def load_bpf_prog(shield_name, event, fn_name, src_file, description=None):
    shield_name = shield_name.upper()
    if description is not None:
        logger.info(f"\t[ ] {shield_name} Shield function: {description}")
    logger.info(f"\t[ ] {shield_name}: loading kernel space src: {src_file}")

    b = BPF(src_file)

    logger.info(
        f"\t[ ] {shield_name}: attaching krpobe \n\t\tevent: {event} \n\t\tfunction: {fn_name}"
    )

    b.attach_kprobe(event, fn_name=fn_name)

    logger.info(f"\t[*] {shield_name}: monitoring\n")
    return b


def load_shield_config(shield_name):
    shield_config_name = shield_name.lower() + constants.SHIELD_CONFIG_EXT
    shield_config_file = None
    for root, dirs, files in os.walk(constants.SHIELD_PATH):
        for file in files:
            if file == shield_config_name:
                shield_config_file = os.path.join(root, file)

    if shield_config_file is not None:
        f = open(shield_config_file, "rb")
        return tomllib.load(f)
    else:
        message = f"no toml configuration file for {shield_name} Shield;\n check that {shield_name}.toml exists on same directory than bpf python script"
        raise ShieldConfigurationError(message)
