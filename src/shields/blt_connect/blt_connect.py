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

# shield name
# must be same with in toml root config
SHIELD_NAME="blt_connect"

# kernel section

# kprobe event name
event="hci_conn_request_evt"
# c function for the kprobe
fn_name="blt_connect_observer"
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
                blt_connect_data = (
                        # "dev_name:%s-addr:%s-name:%s-conn_dev_addr:%s-conn_dev_class:%s-pid:%d"
                        "dev_name:%s-name:%s-addr:%s-%s:%s:%s:%s:%s:%s:"
                                    %
                                    (event.hci_dev_name.decode("utf-8", "replace"),
                                     event.name.decode("utf-8", "replace"),
                                     bytearray(event.hci_dev_bdaddr).hex(),
                                     bytearray(event.hci_dev_bdaddr[0]).hex(),
                                     bytearray(event.hci_dev_bdaddr[1]).hex(),
                                     bytearray(event.hci_dev_bdaddr[2]).hex(),
                                     bytearray(event.hci_dev_bdaddr[3]).hex(),
                                     bytearray(event.hci_dev_bdaddr[4]).hex(),
                                     bytearray(event.hci_dev_bdaddr[5]).hex(),
                                     # event.hci_dev_bdaddr.decode("utf-8", "replace"),
                                     # event.conn_dev_addr.decode("utf-8", "replace"),
                                     # event.conn_dev_class.decode("utf-8", "replace"),
                                     # event.pid
                                     )
                                    )


                    
                message = ""
                try:

                    message = f"{constants.CAETRA_SENDER_LABEL}_{SHIELD_NAME.upper()} act: '{shield_config.get("action_label")}' data: { blt_connect_data }"

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
