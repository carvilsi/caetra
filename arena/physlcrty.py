#!/usr/bin/env python

from bcc import BPF

# define BPF program
prog = """
#include <linux/sched.h>

struct data_t {
    u32 pid;
    u64 ts;
    char comm[TASK_COMM_LEN];
};

BPF_PERF_OUTPUT(events);

int usb(struct pt_regs *ctx)
{
	struct data_t data = {};

    data.pid = bpf_get_current_pid_tgid();
    data.ts = bpf_ktime_get_ns();
    bpf_get_current_comm(&data.comm, sizeof(data.comm));

    events.perf_submit(ctx, &data, sizeof(data));

    return 0;
}

"""

# load BPF program
b = BPF(text=prog)
# b.attach_kprobe(event=b.get_syscall_fnname("inotify_add_watch"), fn_name="hello")
# this one will be possible to filter looking for udevd TODO: check if possible to have a tracepoint
# b.attach_kprobe(event=b.get_syscall_fnname("openat"), fn_name="hello")
# XXX: This works for USB
# b.attach_kprobe(event="usb_bus_notify", fn_name="usb")
b.attach_kprobe(event="hid_report_raw_event", fn_name="usb")
# b.attach_kprobe(event=b.get_syscall_fnname("keyctl"), fn_name="hello")

# header
print("%-18s %-16s %-6s %s" % ("TIME(s)", "COMM", "PID", "MESSAGE"))

def print_event(cpu, data, size):
    event = b["events"].event(data)
    print("%-14.3f %-12s %-6d %s" % ((event.ts/1000000000),
           event.comm, event.pid, "monitoring USB"))

# loop with callback to print_event
b["events"].open_perf_buffer(print_event)
while 1:
    try:
        b.perf_buffer_poll()
        # (task, pid, cpu, flags, ts, msg) = b.trace_fields()
        # printb(b"%-18.9f %-16s %-6d %s" % (ts, task, pid, msg))
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
