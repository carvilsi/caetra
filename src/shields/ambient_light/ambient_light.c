#include<linux/backlight.h>

struct ambient_light_t {
      // write down here your custom struct vars 
       u32 pid;
};

BPF_PERF_OUTPUT(events);

int ambient_light_observer(struct pt_regs *ctx, struct backlight_device *kstrct)
{
        struct ambient_light_t data = {};
        
        data.pid = bpf_get_current_pid_tgid();

        //bpf_probe_read_kernel_str(data.path, sizeof(data.path), kstrct->something);

        events.perf_submit(ctx, &data, sizeof(data));

        return 0;
}
