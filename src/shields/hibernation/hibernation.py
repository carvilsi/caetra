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
from caetra_exceptions import ShieldConfigurationError, ConfigurationError, MaxRetriesReached
from logging_handler import log_shield_exception, log_shield_exception_warn
from senders_handler import send
import constants
import status_handler

# shield name
# must be same with in toml root config
SHIELD_NAME = "hibernation"

# kernel section

# kprobe event name
event = "unregister_pm_notifier"
# c function for the kprobe
fn_name = "hibernation_observer"
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
            def shield_logic(ts, pid):

                # get here the data for shield impl
                hibernation_data = ("ts:%s-pid:%d" % (pid, ts))
                    
                message = f"{constants.CAETRA_SENDER_LABEL}_{SHIELD_NAME.upper()} act: '{shield_config.get("action_label")}' data: { hibernation_data }"
                try:
                    if shield_config["features"]["wait_connection_sending"]:
                        if status.is_there_connection(shield_config["features"]["max_retries"], shield_config["features"]["wait_to_try"]):
                    
                            send(message, shield_config)
                except ConfigurationError as e:
                    log_shield_exception(e, SHIELD_NAME)
                except MaxRetriesReached as e: 
                    log_shield_exception(e, SHIELD_NAME)
                else:
                    logger_shields.info(
                        f"{SHIELD_NAME} triggered and sent: {message}"
                    )
                finally:
                    logger_shields.warning(f"{SHIELD_NAME} triggered: {message}")

            while 1:
                try:

                    (task, pid, cpu, flags, ts, msg) = b.trace_fields()
                    shield_logic(ts, pid)
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
