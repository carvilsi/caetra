// this is need it since current version of 
// bcc v0.35.0 supports Linux up to 6.14 and
// right now running on a 6.18.5 kernel.
// check: https://github.com/iovisor/bcc/issues/5444#issuecomment-3772446064

struct bpf_task_work {
        __u64 __opaque;
} __attribute__((aligned(8)));


