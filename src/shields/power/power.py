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

# from linux/power_supply.h
POWER_SUPPLY_TYPE = {
        0: "POWER_SUPPLY_TYPE_UNKNOWN",
        1: "POWER_SUPPLY_TYPE_BATTERY",
        2: "POWER_SUPPLY_TYPE_UPS",
        3: "POWER_SUPPLY_TYPE_MAINS",
        4: "POWER_SUPPLY_TYPE_USB",              # [> Standard Downstream Port <]
        5: "POWER_SUPPLY_TYPE_USB_DCP",          # [> Dedicated Charging Port <]
        6: "POWER_SUPPLY_TYPE_USB_CDP",          # [> Charging Downstream Port <]
        7: "POWER_SUPPLY_TYPE_USB_ACA",          # [> Accessory Charger Adapters <]
        8: "POWER_SUPPLY_TYPE_USB_TYPE_C",       # [> Type C Port <]
        9: "POWER_SUPPLY_TYPE_USB_PD",           # [> Power Delivery Port <]
        10: "POWER_SUPPLY_TYPE_USB_PD_DRP",      # [> PD Dual Role Port <]
        11: "POWER_SUPPLY_TYPE_APPLE_BRICK_ID",  # [> Apple Charging Method <]
        12: "POWER_SUPPLY_TYPE_WIRELESS",        # [> Wireless <]
}


# shield name
# must be same with in toml root config
SHIELD_NAME="power"

# kernel section

# kprobe event name
event="power_supply_changed"
# c function for the kprobe
fn_name="power_observer"
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
                SHIELD_NAME,
                event,
                fn_name,
                src_file,
                shield_config.get("description"),
                shield_config.get("features"),
            )

            # Write here the logic for your shield
            def shield_logic(cpu, data, size):
                event = b["events"].event(data)

                # get here the data for shield impl
                power_data = ("name:%s-type:%s-pid:%d"
                              %
                                (
                                  event.name.decode("utf-8", "replace"),
                                  POWER_SUPPLY_TYPE[event.type],
                                  event.pid
                                )
                             )
                    
                message = f"{constants.CAETRA_SENDER_LABEL}_{SHIELD_NAME.upper()} act: '{shield_config.get("action_label")}' data: { power_data }"
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
