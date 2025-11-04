#!/usr/bin/env python

from bcc import BPF
from bcc.utils import printb

# load BPF program
b = BPF(src_file="general_monitor.c")
# XXX: This works for USB
b.attach_kprobe(event="usb_notify_add_device", fn_name="usb_monitor")
# b.attach_kprobe(event="xhci_bus_resume", fn_name="general_monitor")
# b.attach_kprobe(event="hid_report_raw_event", fn_name="hdi_monitor")
# b.attach_kprobe(event="input_handle_event", fn_name="general_monitor")
# b.attach_kprobe(event="power_supply_changed", fn_name="pwr_monitor")

print("eBPFphysec with <3 by (#4|2 \n monitoring...\n") 

while 1:
    try:
        (task, pid, cpu, flags, ts, msg) = b.trace_fields()
        printb(b"%-18.9f %-16s %-6d %s" % (ts, task, pid, msg))
        power_type = b["power"]
        for k, v in power_type.items():
            print(f"{k.foo} -> {v.value}");
    except ValueError:
        continue
    except KeyboardInterrupt:
        exit()

