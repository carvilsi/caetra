#include<linux/power_supply.h>

struct power_t {
       u32 pid;
       char name[5];
       int type;
};

BPF_PERF_OUTPUT(events);

int power_observer(struct pt_regs *ctx, struct power_supply *kstrct)
{
        struct power_t data = {};
        
        data.pid = bpf_get_current_pid_tgid();
        data.type = kstrct->desc->type;

        bpf_probe_read_kernel_str(data.name, sizeof(data.name), kstrct->desc->name);

        events.perf_submit(ctx, &data, sizeof(data));

        return 0;
}
