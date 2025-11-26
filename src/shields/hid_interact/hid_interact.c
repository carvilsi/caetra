#include<linux/hid.h>

struct hid_move_t {
        u32 pid;
        u64 ts;
        int rtype;
        u16 vendor;
        u32 prod;
};

BPF_PERF_OUTPUT(events);

int hid_move_observer(struct pt_regs *ctx, struct hid_device *kstrct)
{
        struct hid_move_t data = {};
        
        data.pid = bpf_get_current_pid_tgid();
        data.ts = bpf_ktime_get_ns();
        data.rtype = kstrct->type; 
        data.vendor = kstrct->vendor;
        data.prod = kstrct->product;

        events.perf_submit(ctx, &data, sizeof(data));

        return 0;
}
