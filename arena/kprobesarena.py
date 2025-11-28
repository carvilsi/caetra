#!/usr/bin/env python

from bcc import BPF
from bcc.utils import printb

import datetime

# load BPF program
b = BPF(src_file="general_monitor.c")
# XXX: This works for USB
# b.attach_kprobe(event="usb_notify_add_device", fn_name="usb_monitor")

# b.attach_kprobe(event="xhci_bus_resume", fn_name="general_monitor")
# b.attach_kprobe(event="hid_report_raw_event", fn_name="hdi_monitor")
# b.attach_kprobe(event="input_handle_event", fn_name="general_monitor")

# power
# b.attach_kprobe(event="power_supply_changed", fn_name="pwr_monitor")

# XXX: Works when attaching SD
# b.attach_kprobe(event="mmc_attach_sd", fn_name="sdcard_observer")
# XXX: only works on remove SDCard
# b.attach_kprobe(event="mmc_sd_alive", fn_name="sdcard_observer")

# XXX: works when attaching SDCard and get data about the card
# b.attach_kprobe(event="mmc_sd_runtime_suspend", fn_name="sdcard_observer")

# hid 
## attach
# b.attach_kprobe(event="hid_add_device", fn_name="hid_monitor")

## remove
# b.attach_kprobe(event="hid_device_remove", fn_name="hid_monitor_remove")

## Bluetooth 
# XXX: works on pair and connect
# b.attach_kprobe(event="hci_conn_request_evt", fn_name="bt_connect_monitor")

# XXX: works on disconnect or unpair
# b.attach_kprobe(event="hci_disconn_complete_evt", fn_name="bt_disconnect_monitor")

## input input_handle_event
# XXX: gets any interaction keyboard, trackpad, etc...
# b.attach_kprobe(event="input_handle_event", fn_name="input_monitor")

## suspend hibernation
# XXX: works on resuming from hibernation
# b.attach_kprobe(event="unregister_pm_notifier", fn_name="hibernation_monitor")

## ambient light changed
# XXX: works when the ambient light changes, only working on Mac Book Pro
# b.attach_kprobe(event="backlight_device_set_brightness", fn_name="light_monitor")

### TODO: to implement on caetra
## input  inet_dev
# XXX: gets any interaction on ip changes inet
b.attach_kprobe(event="inet_alloc_ifa", fn_name="inet_monitor")
b.attach_kprobe(event="inetdev_event", fn_name="inet_event_monitor")


print("eBPFphysec with <3 by (#4|2 \n monitoring...\n") 
print(datetime.datetime.now())

while 1:
    try:
        (task, pid, cpu, flags, ts, msg) = b.trace_fields()
        printb(b"%-18.9f %-16s %-6d %s" % (ts, task, pid, msg))
        # print(datetime.datetime.now())
        
    except ValueError:
        exit()

