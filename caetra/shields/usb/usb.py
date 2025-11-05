#!/usr/bin/env python
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../utils')))

from shields import deploying
from logger_setup import logger_shields
from bcc.utils import printb
from time import strftime

SHIELD_NAME="USB"
SHIELD_DESCRIPTION="""
\t\tWhen a USB device is attached will do several things
"""

# kernel section
event="usb_notify_add_device"
fn_name="usb_observer"
src_file="usb.c"

def bpf_main():

    b = deploying.load_bpf_prog(SHIELD_NAME, event, fn_name, src_file, SHIELD_DESCRIPTION)
    
    def print_event(cpu, data, size):
        event = b["events"].event(data)
        logger_shields.warning("%-9s %-7d %s" % (strftime("%H:%M:%S"), event.pid,
                                event.path.decode('utf-8', 'replace')))
    
    # TODO: de-authorize here: /sys/bus/usb/devices/{event.path}/authorized
    
    b["events"].open_perf_buffer(print_event)
    while 1:
        try:
            b.perf_buffer_poll()
        except ValueError:
            continue
        except KeyboardInterrupt:
            exit()
    
if __name__ == "__main__":
    bpf_main()
