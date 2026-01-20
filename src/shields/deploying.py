from bcc import BPF
from logger_setup import logger
import tomllib
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../utils"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
import constants
from caetra_exceptions import ShieldConfigurationError
from dict_handler import validate_dict_structure


# returns a BPF program loaded and attached to kernel
# also does some logging for user feedback
def load_bpf_prog(
    shield_name, event, fn_name, src_file, description=None, shield_features=None
):
    shield_name = shield_name.upper()
    if description is not None:
        logger.info(f"\t[ ] {shield_name} Shield function: {description}")

    if shield_features is not None:
        for key, value in shield_features.items():
            logger.info(
                f"\t[ ] {shield_name} Shield feature: '{key}' -> {'Enabled [x]' if value else 'Disabled [-]'}"
            )

    logger.info(f"\t[ ] {shield_name}: loading kernel space src: {src_file}")

    include_path = os.path.join(os.path.realpath("."), 'src', 'shields')
    cflag_include = f"-I{include_path}/"

    b = BPF(src_file, cflags=[cflag_include])

    logger.info(
        f"\t[ ] {shield_name}: attaching krpobe: \n\t\t\t\t\t\t\tevent: {event} \n\t\t\t\t\t\t\tfunction: {fn_name}"
    )

    if isinstance(event, list):
        if not isinstance(fn_name, list) or len(fn_name) != len(event):
            errmsg = f"since there are more than one event {event} for {shield_name}, 'fn_name' {fn_name} must have same amount of elements"
            raise ShieldConfigurationError(errmsg)
        for i, evn in enumerate(event):
            b.attach_kprobe(evn, fn_name=fn_name[i])
    else:
        b.attach_kprobe(event, fn_name=fn_name)

    logger.info(f"\t[*] {shield_name}: monitoring\n")
    return b

# checks for mandatory configuration varialbes
def shield_config_check(shield_config, shield_name):
    validate_dict_structure(
            constants.CONFIG_SHIELD_MANDATORY,
            shield_config,
            shield_name
    )
    logger.debug(f"Shield {shield_name.upper()} Configuration file OK")


def load_shield_config(shield_name):
    shield_config_name = shield_name.lower() + constants.SHIELD_CONFIG_EXT
    shield_config_file = None
    for root, dirs, files in os.walk(constants.SHIELD_PATH):
        for file in files:
            if file == shield_config_name:
                shield_config_file = os.path.join(root, file)

    if shield_config_file is not None:
        f = open(shield_config_file, "rb")
        shield_config = tomllib.load(f)
        shield_config_check(shield_config.get(shield_name), shield_name)
        return shield_config
    else:
        message = f"no toml configuration file for {shield_name} Shield;\n check that {shield_name}.toml exists on same directory than bpf python script"
        raise ShieldConfigurationError(message)
