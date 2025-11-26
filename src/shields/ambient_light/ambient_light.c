#include<linux/backlight.h>

#define MAX_LEN 80 

struct ambient_light_t {
        u32 pid;
        u64 ts;
        char name[MAX_LEN];
        int brightness;
        int type;
};

BPF_PERF_OUTPUT(events);

int ambient_light_observer(struct pt_regs *ctx, struct backlight_device *kstrct)
{
        struct ambient_light_t data = {};
        
        data.pid = bpf_get_current_pid_tgid();
        data.ts = bpf_ktime_get_ns();
        data.brightness = kstrct->props.brightness;
        data.type = kstrct->props.type;

        bpf_probe_read_kernel_str(data.name, sizeof(data.name), kstrct->dev.kobj.name);

        events.perf_submit(ctx, &data, sizeof(data));

        return 0;
}
