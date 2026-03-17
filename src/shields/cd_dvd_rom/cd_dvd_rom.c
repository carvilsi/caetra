#include <kernel_additions_headers.h>

struct cd_dvd_rom_t {
        u32 pid;
	u64 ts;
};

BPF_PERF_OUTPUT(events);

int cd_dvd_rom_observer(struct pt_regs *ctx)
{
        struct cd_dvd_rom_t data = {};
        
        data.pid = bpf_get_current_pid_tgid();
	data.ts = bpf_ktime_get_ns();

        events.perf_submit(ctx, &data, sizeof(data));

        return 0;
}
