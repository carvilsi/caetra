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

# from linux/hid.h
HID_TYPE = {
        0: "HID_TYPE_OTHER",
        1: "HID_TYPE_USBMOUSE",
        2: "HID_TYPE_USBNONE",
}

# shield name
# must be same with in toml root config
SHIELD_NAME = "hid_add_remove"

# kernel section

# kprobe event name
events = ["hid_add_device", "hid_device_remove"]
# c function for the kprobe
fns_name = ["hid_add_observer", "hid_remove_observer"]

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
                events,
                fns_name,
                src_file,
                shield_config.get("description"),
                shield_config.get("features"),
            )
            
            # Write here the logic for your shield
            def shield_logic(cpu, data, size):
                event = b["events"].event(data)

                message = ""
                match event.act_type:
                    case constants.HID_ADD_ACT:
                        hid_add_data = (
                                "bus:%d-vendor:%d-prod:%d-vers:%d-type:%s-name:%s-phys:%s-path:%s-pid:%d"
                            % (
                                event.bus,
                                event.vendor,
                                event.prod,
                                event.vers,
                                HID_TYPE[event.type],
                                event.name.decode("utf-8", "replace"),
                                event.phys.decode("utf-8", "replace"),
                                event.path.decode("utf-8", "replace"),
                                event.pid,
                            )
                        )
                            
                        message = f"{constants.CAETRA_SENDER_LABEL}_{SHIELD_NAME.upper()} act: '{shield_config.get("action_label")} {shield_config.get("action_add")}' data: { hid_add_data }"

                    case constants.HID_REMOVE_ACT:
                        hid_remove_data = (
                                "name:%s-path:%s-type:%s-pid:%d"
                            % (
                                event.name.decode("utf-8", "replace"),
                                event.path.decode("utf-8", "replace"),
                                event.type_remove.decode("utf-8", "replace"),
                                event.pid,
                            )
                        )

                        message = f"{constants.CAETRA_SENDER_LABEL}_{SHIELD_NAME.upper()} act: '{shield_config.get("action_label")} {shield_config.get("action_remove")}' data: { hid_remove_data }"
                    case _:
                        # TODO implement error
                        print("unknown action")

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
            # b_remove["events_remove"].open_perf_buffer(shield_logic)
            while 1:
                try:
                    b.perf_buffer_poll()
                    # b_remove.perf_buffer_poll()
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

