// this is need it since current version of 
// bcc v0.35.0 supports Linux up to 6.14 and
// right now running on a 6.18.5 kernel.
// check: https://github.com/iovisor/bcc/issues/5444#issuecomment-3772446064
#ifndef bpf_task_work 
#define bpf_task_work 

struct bpf_task_work {
        __u64 __opaque;
} __attribute__((aligned(8)));

#endif // bpf_task_work

// this is need it to run it on 24.04.1-Ubuntu (noble)
// with kernel Linux 6.14.0-37-generic 
#ifndef bpf_wq
#define bpf_wq

struct bpf_wq {
	__u64 __opaque[2];
} __attribute__((aligned(8)));

#endif // bpf_wq 
