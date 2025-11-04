#!/usr/bin/env python

from bcc import BPF
from bcc.utils import printb

# define BPF program

prog = """
#include <linux/input.h>
#include <uapi/linux/input-event-codes.h>

int klogger(struct pt_regs *ctx, struct input_dev *dev,
                   unsigned int type, unsigned int code, int value) {
    
    bpf_trace_printk("%d\\t%d\\t%d\\n", type, code, value);
    return 0;
}

"""

# load BPF program
b = BPF(text=prog)
# XXX: This works for USB
b.attach_kprobe(event="input_handle_event", fn_name="klogger")


# def print_event(cpu, data, size):
    # event = b["events"].event(data)
    # printb(b"%-14.3f %-12s %-6d %d" % ((event.ts/1000000000),
           # event.comm, event.pid, event.uid))

# loop with callback to print_event
# b["events"].open_perf_buffer(print_event)
while 1:
    try:
        # b.perf_buffer_poll()
        (task, pid, cpu, flags, ts, msg) = b.trace_fields()
        printb(b"%-18.9f %-16s %-6d %s" % (ts, task, pid, msg))
    except ValueError:
        continue
    except KeyboardInterrupt:
        exit()

# format output
# while 1:
    # try:
        # (task, pid, cpu, flags, ts, msg) = b.trace_fields()
    # except ValueError:
        # continue
    # except KeyboardInterrupt:
        # exit()
