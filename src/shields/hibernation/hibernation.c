#include<none>

struct hibernation_t {
      // write down here your custom struct vars 
       u32 pid;
};

BPF_PERF_OUTPUT(events);

int hibernation_observer(struct pt_regs *ctx, struct none *kstrct)
{
        struct hibernation_t data = {};
        
        data.pid = bpf_get_current_pid_tgid();

        //bpf_probe_read_kernel_str(data.path, sizeof(data.path), kstrct->something);

        events.perf_submit(ctx, &data, sizeof(data));

        return 0;
}
