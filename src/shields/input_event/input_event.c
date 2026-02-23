#include<linux/input.h>

#include <kernel_additions_headers.h>

#define MAX_LEN 120

struct input_event_t {
        u32 pid;
        u64 ts;
        char name[MAX_LEN];
        char input_name[MAX_LEN];
        int code;
        char phys[MAX_LEN];
};

BPF_PERF_OUTPUT(events);

int input_event_observer(struct pt_regs *ctx, struct input_dev *kstrct, int arg1, int arg2, int arg3)
{
        struct input_event_t data = {};
        
        data.pid = bpf_get_current_pid_tgid();
        data.ts = bpf_ktime_get_ns();

        bpf_probe_read_kernel_str(data.name, sizeof(data.name), kstrct->name);
        bpf_probe_read_kernel_str(data.input_name, sizeof(data.input_name), kstrct->dev.kobj.name);
        bpf_probe_read_kernel_str(data.phys, sizeof(data.phys), kstrct->phys);

        data.code = arg2;

        events.perf_submit(ctx, &data, sizeof(data));

        return 0;
}

