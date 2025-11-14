#include<linux/device.h>

struct hid_remove_t {
      // write down here your custom struct vars 
       u32 pid;
       u64 ts;
};

BPF_PERF_OUTPUT(events);

int hid_remove_observer(struct pt_regs *ctx, struct device *kstrct)
{
        struct hid_remove_t data = {};
        
        data.pid = bpf_get_current_pid_tgid();
        //data.ts = bpf_ktime_get_ns();
        //
        //bpf_probe_read_kernel_str(data.path, sizeof(data.path), kstrct->something);

        events.perf_submit(ctx, &data, sizeof(data));

        return 0;
}
