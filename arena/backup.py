#!/usr/bin/env python

from bcc import BPF
from bcc.utils import printb
import time

import usb_shield
import sdcard_shield

# define BPF program
prog = """

// Monitoring USB
int usb_monitor(struct pt_regs *ctx)
{
    bpf_trace_printk("usb_actn");

    return 0;
}

// Monitoring SDCard
int sdcard_monitor(struct pt_regs *ctx)
{
    bpf_trace_printk("sdcard_actn");

    return 0;
}

// Monitoring Suspension/Hibernation 
int hibernation_monitor(struct pt_regs *ctx)
{
    bpf_trace_printk("hibernation_actn");

    return 0;
}

// Monitoring HID
int hid_monitor(struct pt_regs *ctx)
{
    bpf_trace_printk("hid_actn");

    return 0;
}

// Monitoring Bluetooth
int blt_monitor(struct pt_regs *ctx)
{
    bpf_trace_printk("blt_actn");

    return 0;
}

// Monitoring Power Supply
int pwr_monitor(struct pt_regs *ctx)
{
    bpf_trace_printk("pwr_actn");

    return 0;
}

"""

# load BPF program
b = BPF(text=prog)

# USB
# someone attched a usb device to a port
b.attach_kprobe(event="usbdev_notify", fn_name="usb_monitor")

# SDCard
# someone attached a SDCard to the slot reader
b.attach_kprobe(event="mmc_attach_sd", fn_name="sdcard_monitor")

# Resuming from suspension/hiberbnation
# someone tries to resume from suspension/hibernation
b.attach_kprobe(event="xhci_bus_resume", fn_name="hibernation_monitor")

# HID
# someone has interacted with HID, mouse, trackpad, keyboards...
# this will require to wait some time, otherwise will be
# triggered from the start
# TODO: uncomment this
time.sleep(10)
b.attach_kprobe(event="input_handle_event", fn_name="hid_monitor")

# Bluetooth 
# someone has connected or trying to bind to bluetooth device...
b.attach_kprobe(event="mgmt_device_connected", fn_name="blt_monitor")

# Power Supply 
# the power supply has been changed, maybe someone did it
b.attach_kprobe(event="power_supply_changed", fn_name="pwr_monitor")


while 1:
    try:
        (task, pid, cpu, flags, ts, msg) = b.trace_fields()

        match msg:
            case b"usb_actn":
                # TODO: implement action
                print("usb")
            case b"sdcard_actn":
                # TODO: implement action
                print("sdcard")
            case b"hibernation_actn":
                # TODO: implement action
                print("hibernation")
            case b"hid_actn":
                # TODO: implement action
                print("hid")
            case b"blt_actn":
                # TODO: implement action
                print("bluetooth")
            case b"pwr_actn":
                # TODO: implement action
                print("power")

    except ValueError:
        continue
    except KeyboardInterrupt:
        exit()

