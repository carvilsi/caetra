#!/usr/bin/env python

from bcc import BPF
from bcc.utils import printb

# define BPF program
prog = """
#include <linux/sched.h>

int hello(void *ctx) {
    bpf_trace_printk("Hello, World!\\n");
    return 0;
}

"""

# load BPF program
b = BPF(text=prog)
# b.attach_kprobe(event=b.get_syscall_fnname("inotify_add_watch"), fn_name="hello")
# this one will be possible to filter looking for udevd TODO: check if possible to have a tracepoint
# b.attach_kprobe(event=b.get_syscall_fnname("openat"), fn_name="hello")
# XXX: This works for USB
b.attach_kprobe(event="usb_bus_notify", fn_name="hello")
# b.attach_kprobe(event=b.get_syscall_fnname("keyctl"), fn_name="hello")

# header

while 1:
    try:
        (task, pid, cpu, flags, ts, msg) = b.trace_fields()
        printb(b"%-18.9f %-16s %-6d %s" % (ts, task, pid, msg))
    except ValueError:
        continue
    except KeyboardInterrupt:
        exit()

