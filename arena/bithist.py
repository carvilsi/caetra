#!/usr/bin/env python3

from __future__ import print_function
from bcc import BPF
from time import sleep

# load BPF program
b = BPF(text="""
#include <uapi/linux/ptrace.h>
#include <linux/blkdev.h>

BPF_HISTOGRAM(dist);

int kprobe__blk_account_io_done(struct pt_regs *ctx, struct request *req)
{
	dist.increment(bpf_log2l(req->__data_len / 1024));
	return 0;
}
""")

if BPF.get_kprobe_functions(b'__blk_account_io_done'):
    # __blk_account_io_done is available before kernel v6.4.
    b.attach_kprobe(event="__blk_account_io_done", fn_name="trace_req_done")
elif BPF.get_kprobe_functions(b'blk_account_io_done'):
    # blk_account_io_done is traceable (not inline) before v5.16.
    b.attach_kprobe(event="blk_account_io_done", fn_name="trace_req_done")
else:
    b.attach_kprobe(event="blk_mq_end_request", fn_name="trace_req_done")

# header
print("Tracing... Hit Ctrl-C to end.")

# trace until Ctrl-C
try:
	sleep(99999999)
except KeyboardInterrupt:
	print()

# output
b["dist"].print_log2_hist("kbytes")
