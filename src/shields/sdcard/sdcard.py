# generic imports
import sys
import os

# caetra imports
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../../utils"))
from shields import deploying
from logger_setup import logger_shields, logger
from caetra_exceptions import ShieldConfigurationError

# shield name
# must be same with in toml root config
SHIELD_NAME = "sdcard"

# kernel section

# kprobe event name
event = "mmc_attach_sd"
# c function for the kprobe
fn_name = "sdcard_observer"
# c source file; the name must be the same that the Shield name
src_file = SHIELD_NAME + ".c"


def bpf_main():
    try:
        # shield configuration
        config = deploying.load_shield_config(SHIELD_NAME)
        shield_config = config.get(SHIELD_NAME)

        # BPF object
        b = deploying.load_bpf_prog(
            SHIELD_NAME, event, fn_name, src_file, shield_config.get("description")
        )

        while 1:
            try:
                (task, pid, cpu, flags, ts, msg) = b.trace_fields()
                logger_shields.warning(f"{msg}")
            except ValueError:
                continue
            except KeyboardInterrupt:
                exit()
    except ShieldConfigurationError as e:
        msg = "[!] " + SHIELD_NAME.upper() + " " + str(e)
        logger.error(e)
        logger_shields.error(msg)
    except Exception as e:
        logger.error(e)
        msg = "[!] " + SHIELD_NAME.upper() + " " + str(e)
        logger_shields.error(msg)


if __name__ == "__main__":
    bpf_main()
