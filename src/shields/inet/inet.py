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
from caetra_exceptions import ShieldConfigurationError, ConfigurationError, MaxActionReached, MaxRetriesReached, NoInternetConnection
from logging_handler import log_shield_exception, log_shield_exception_warn
from senders_handler import send
from blt_utils import mac_address_format
import constants
import status_handler

# from linux/netdevice.h
# only interesting events
NETDEV_EVENTS = {
        1:  "NETDEV_UP",
        2:  "NETDEV_DOWN", 
        3:  "NETDEV_REBOOT",
        4:  "NETDEV_CHANGE",
        11: "NETDEV_CHANGENAME",
}

# shield name
# must be same with in toml root config
SHIELD_NAME = "inet"

# kernel section

# kprobe event name
events = ["inet_alloc_ifa", "inetdev_event"]
# events = ["inetdev_event"]
# c function for the kprobe
fns_name = ["inet_alloc_observer", "inet_event_observer"]
# fns_name = ["inet_event_observer"]

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
                events,
                fns_name,
                src_file,
                shield_config.get("description"),
                shield_config.get("features"),
            )
            
            # Write here the logic for your shield
            def shield_logic(cpu, data, size):
                event = b["events"].event(data)

                inet_event_type = event.inet_evnt;

                message = ""
                # an inetdev_event
                if inet_event_type > 0:
                    # a NETDEV_UP
                    if inet_event_type != 1:
                        inet_data = ("pid:%d" % (event.pid))
                        
                        message = f"{constants.CAETRA_SENDER_LABEL}_{SHIELD_NAME.upper()} act: '{shield_config.get("action_label").upper()} {NETDEV_EVENTS[inet_event_type]}' data: {inet_data}"

                # inet_alloc_ifa
                else:
                    inet_data = (
                                "name:%s-mac_addr:%s-pid:%d"
                            % (
                                event.name.decode("utf-8", "replace"),
                                mac_address_format(bytearray(event.mac_addr).hex().upper()),
                                event.pid,
                            )
                        )

                    message = f"{constants.CAETRA_SENDER_LABEL}_{SHIELD_NAME.upper()} act: '{shield_config.get("action_label").upper()} {NETDEV_EVENTS[1]}' data: {inet_data}"
                try:
                    if inet_event_type == 2:
                        message = f"{SHIELD_NAME} triggered NETDEV_DOWN, no internet, not possible to send now: {message}"
                        raise NoInternetConnection(message)
                    if shield_config["features"]["wait_connection_sending"]:
                        if inet_event_type > 1 and shield_config["features"]["limit_sending"]:
                            if status.is_there_connection(shield_config["features"]["max_retries"], shield_config["features"]["wait_to_try"]):
                                status.can_be_sent(event.ts, shield_config["features"]["max_actions"], shield_config["features"]["cool_down_time"])

                    send(message, shield_config)
                except ConfigurationError as e:
                    log_shield_exception(e, SHIELD_NAME)
                except MaxActionReached as e:
                    log_shield_exception_warn(e, SHIELD_NAME)
                except MaxRetriesReached as e:
                    log_shield_exception_warn(e, SHIELD_NAME)
                except NoInternetConnection as e:
                    log_shield_exception_warn(e, SHIELD_NAME)
                finally:
                    if len(message) != 0:
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

