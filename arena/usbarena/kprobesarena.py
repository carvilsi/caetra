#!/usr/bin/env python

from bcc import BPF
from bcc.utils import printb
from time import strftime

# from linux/mmc/card.h
MMC_TYPE = {
        0: "MMC_TYPE_MMC",        # [> MMC card <]
        1: "MMC_TYPE_SD",         # [> SD card <]
        2: "MMC_TYPE_SDIO",       # [> SDIO card <]
        3: "MMC_TYPE_SD_COMBO",   # [> SD combo (IO+mem) card <]
}

# load BPF program
b = BPF(src_file="general_monitor.c")
# XXX: This works for USB
# b.attach_kprobe(event="usb_notify_add_device", fn_name="usb_monitor")
# XXX: only works on remove SDCard
# b.attach_kprobe(event="mmc_sd_alive", fn_name="sdcard_observer")

# XXX: works when attaching SDCard and get data about the card
b.attach_kprobe(event="mmc_sd_runtime_suspend", fn_name="sdcard_observer")

print("eBPFphysec with <3 by (#4|2 \n monitoring...\n") 

def shield_logic(cpu, data, size):
    event = b["events"].event(data)

    print("dev_name: %s\tclass_name: %s\tdev_path0: %s\tdev_path1: %s\tmmc_type: %d\tprod_name: %s\tyear: %d\tserial: %d\tmanfid: %d\toemid: %d"
            % (
                event.dev_name.decode("utf-8", "replace"),
                event.class_name.decode("utf-8", "replace"),
                event.dev_path0.decode("utf-8", "replace"),
                event.dev_path1.decode("utf-8", "replace"),
                event.mmc_type,
                event.prod_name.decode("utf-8", "replace"),
                event.mmc_year,
                event.mmc_serial,
                event.mmc_manfid,
                event.mmc_oemid,
              )
         )

    print("mmc type: " + MMC_TYPE[event.mmc_type])

b["events"].open_perf_buffer(shield_logic)
while 1:
    try:
        b.perf_buffer_poll()
    except ValueError:
        continue
    except KeyboardInterrupt:
        exit()

