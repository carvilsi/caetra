# generic imports
import sys
import os

# caetra imports
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../../utils"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../../senders"))
from shields import deploying
from logger_setup import logger_shields
from caetra_exceptions import ShieldConfigurationError, ConfigurationError, MaxActionReached
from logging_handler import log_shield_exception, log_shield_exception_warn
from senders_handler import send
import constants
import status_handler

# shield name
# must be same with in toml root config
SHIELD_NAME="ambient_light"

# kernel section

# kprobe event name
event="backlight_device_set_brightness"
# c function for the kprobe
fn_name="ambient_light_observer"
# c source file; the name must be the same that the Shield name
src_file = SHIELD_NAME + ".c"

status = status_handler.StatusHandler()

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
                ambient_light_data = (
                        "name:%s-brightness:%d-type:%d-pid:%d" %
                           (event.name.decode("utf-8", "replace"),
                            event.brightness,
                            event.type,
                            event.pid)
                        )

                message = f"{constants.CAETRA_SENDER_LABEL}_{SHIELD_NAME.upper()} act: '{shield_config.get("action_label")}' limit_sending: {shield_config["features"]["limit_sending"]} data: { ambient_light_data }"
                try:
                    if shield_config["features"]["limit_sending"]:
                        status.can_be_sent(event.ts, shield_config["features"]["max_actions"], shield_config["features"]["cool_down_time"])

                    send(message, shield_config)
                except ConfigurationError as e:
                    log_shield_exception(e, SHIELD_NAME)
                except KeyboardInterrupt:
                    exit()
                except MaxActionReached as e:
                    log_shield_exception_warn(e, SHIELD_NAME)
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
