# generic imports
import sys
import os
from time import strftime

# caetra imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../utils'))
from shields import deploying
from logger_setup import logger_shields, logger
from caetra_exceptions import ShieldConfigurationError

# shield name
# must be same with in toml root config
SHIELD_NAME="usb"

# kernel section

# kprobe event name
event="usb_notify_add_device"
# c function for the kprobe
fn_name="usb_observer"
# c source file; the name must be the same that the Shield name
src_file= SHIELD_NAME + ".c"

def bpf_main():

    try:
        # shield configuration
        config = deploying.load_shield_config(SHIELD_NAME)
        shield_config = config.get(SHIELD_NAME)
        print(shield_config)

        # BPF object
        b = deploying.load_bpf_prog(SHIELD_NAME, event, fn_name, src_file, shield_config.get('description'))
        
        def print_event(cpu, data, size):
            event = b["events"].event(data)
            logger_shields.warning("%-9s %-7d %s" % (strftime("%H:%M:%S"), event.pid,event.path.decode('utf-8', 'replace')))
        
        # TODO: de-authorize here: /sys/bus/usb/devices/{event.path}/authorized
        
        b["events"].open_perf_buffer(print_event)
        while 1:
            try:
                b.perf_buffer_poll()
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
