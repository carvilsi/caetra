#include <kernel_additions_headers.h>

struct webcam_t {
        u32 pid;
        u64 ts;
};

BPF_PERF_OUTPUT(events);

int webcam_observer(struct pt_regs *ctx)
{
        struct webcam_t data = {};
        
        data.pid = bpf_get_current_pid_tgid();
        data.ts = bpf_ktime_get_ns();

        events.perf_submit(ctx, &data, sizeof(data));

        return 0;
}
