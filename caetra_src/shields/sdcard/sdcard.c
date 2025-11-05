#include<linux/mmc/host.h>

struct key_t {
       char path[5];
       u32 pid;
       u64 ts;
};

BPF_PERF_OUTPUT(events);

int sdcard_observer(struct pt_regs *ctx, struct mmc_host *mmch)
{
        
        bpf_trace_printk("sdcard_actn %s", mmch->class_dev.kobj.name);
        /*struct key_t data = {};*/
        
        /*data.pid = bpf_get_current_pid_tgid();*/
        /*data.ts = bpf_ktime_get_ns();*/
        
        /*bpf_probe_read_kernel_str(data.path, sizeof(data.path), usbd->dev.kobj.name);*/

        /*events.perf_submit(ctx, &data, sizeof(data));*/

        return 0;
}
