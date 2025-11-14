# generic imports
import sys
import os

# caetra imports
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../../utils"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../../senders"))
from shields import deploying
from logger_setup import logger_shields
from caetra_exceptions import ShieldConfigurationError, ConfigurationError
from logging_handler import log_shield_exception
from senders_handler import send
import constants

# from linux/mmc/card.h
# definition fo Multi Media Cards
# TODO: would it better if we can relly on c linux headers for this instead
# hardcoding this types here. Although makes more complex the thing :(
MMC_TYPE = {
    0: "MMC_TYPE_MMC",  # [> MMC card <]
    1: "MMC_TYPE_SD",  # [> SD card <]
    2: "MMC_TYPE_SDIO",  # [> SDIO card <]
    3: "MMC_TYPE_SD_COMBO",  # [> SD combo (IO+mem) card <]
}

# shield name
# must be same with in toml root config
SHIELD_NAME = "mmc"

# kernel section

# kprobe event name
event = "mmc_sd_runtime_suspend"
# c function for the kprobe
fn_name = "mmc_observer"
# c source file; the name must be the same that the Shield name
src_file = SHIELD_NAME + ".c"


def bpf_main():
    try:
        # shield configuration
        config = deploying.load_shield_config(SHIELD_NAME)
        shield_config = config.get(SHIELD_NAME)

        if shield_config.get("enable"):
            # BPF object
            b = deploying.load_bpf_prog(
                SHIELD_NAME, event, fn_name, src_file, shield_config.get("description")
            )

            def shield_logic(cpu, data, size):
                event = b["events"].event(data)

                mmc_data = (
                    "dev_name:%s-prod_name:%s-mmc_type:%s-serial:%d-manfid:%d-oemid:%d-year:%d-class_name:%s-dev_path0:%s-dev_path1:%s"
                    % (
                        event.dev_name.decode("utf-8", "replace"),
                        event.prod_name.decode("utf-8", "replace"),
                        MMC_TYPE[event.mmc_type],
                        event.mmc_serial,
                        event.mmc_manfid,
                        event.mmc_oemid,
                        event.mmc_year,
                        event.class_name.decode("utf-8", "replace"),
                        event.dev_path0.decode("utf-8", "replace"),
                        event.dev_path1.decode("utf-8", "replace"),
                    )
                )

                message = ""
                message = f"{constants.CAETRA_SENDER_LABEL}_{SHIELD_NAME.upper()} act: '{shield_config.get("action_label")}' {mmc_data}"
                try:
                    send(message, shield_config)
                except ConfigurationError as e:
                    log_shield_exception(e, SHIELD_NAME)
                else:
                    logger_shields.info(
                        f"{SHIELD_NAME} triggered and sent: {message}"
                    )
                finally:
                    logger_shields.warning(f"{SHIELD_NAME} triggered: {message}")

            b["events"].open_perf_buffer(shield_logic)
            while 1:
                try:
                    b.perf_buffer_poll()
                except ValueError:
                    continue
                except KeyboardInterrupt:
                    exit()
        else:
            logger_shields.warning("[-] " + SHIELD_NAME.upper() + " Shield disabled.")

    except ShieldConfigurationError as e:
        log_shield_exception(e, SHIELD_NAME)
    except Exception as e:
        log_shield_exception(e, SHIELD_NAME)


if __name__ == "__main__":
    bpf_main()
