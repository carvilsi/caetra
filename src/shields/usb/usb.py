# generic imports
import sys
import os
from time import strftime

# caetra imports
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../../utils"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../../senders"))
from shields import deploying
from logger_setup import logger_shields, logger
from caetra_exceptions import ShieldConfigurationError, ConfigurationError
# from send_canary_dns_token import get_dns_canary_token_call, call_dns_canary_token  
from senders_handler import send

# shield name
# must be same with in toml root config
SHIELD_NAME = "usb"

# kernel section

# kprobe event name
event = "usb_notify_add_device"
# c function for the kprobe
fn_name = "usb_observer"
# c source file; the name must be the same that the Shield name
src_file = SHIELD_NAME + ".c"


def bpf_main():
    try:
        # shield configuration
        config = deploying.load_shield_config(SHIELD_NAME)
        shield_config = config.get(SHIELD_NAME)
        print(shield_config)

        
        if shield_config.get("enable"):
            # BPF object
            b = deploying.load_bpf_prog(
                SHIELD_NAME, event, fn_name, src_file, shield_config.get("description")
            )

            # Write here the logic for your shield
            def shield_logic(cpu, data, size):
                event = b["events"].event(data)

                # raw logging for shield impl
                logger_shields.debug(
                    "%-9s %-7d %s"
                    % (
                        strftime("%H:%M:%S"),
                        event.pid,
                        event.path.decode("utf-8", "replace"),
                    )
                )


                device_path = event.path.decode("utf-8", "replace")
                pid = event.pid

                send("foo bar lol", shield_config.get("senders"))
                
                # if shield_config.get("senders"):
                    # logger_shields.debug("SEND NOTIFICATIONS")
                    
                    # senders_config = shield_config.get("senders")
                    # print(senders_config)
                    # if senders_config.get("canarytokens") and senders_config.get("canarytokens").get("enable"):
                        # canary_call = get_dns_canary_token_call("something: " + device_path + " on process: " + str(pid), senders_config["canarytokens"]["token"]) 
                        # call_dns_canary_token(canary_call)
                # else:
                    # logger_shields.debug("NOT #### SEND NOTIFICATIONS")



            # TODO: de-authorize here: /sys/bus/usb/devices/{event.path}/authorized

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

    except (ShieldConfigurationError,
            ConfigurationError) as e:
        msg = "[!] " + SHIELD_NAME.upper() + " " + str(e)
        logger.error(e)
        logger_shields.error(msg)
    except Exception as e:
        logger.error(e)
        msg = "[!] " + SHIELD_NAME.upper() + " " + str(e)
        logger_shields.error(msg)


if __name__ == "__main__":
    bpf_main()
