#include<linux/device.h>

#define MAX_LEN 20

struct hid_remove_t {
      // write down here your custom struct vars 
       u32 pid;
       char name[MAX_LEN];
       char path[MAX_LEN];
       char type[MAX_LEN];
};

BPF_PERF_OUTPUT(events);

int hid_remove_observer(struct pt_regs *ctx, struct device *kstrct)
{
        struct hid_remove_t data = {};
        
        data.pid = bpf_get_current_pid_tgid();
        bpf_probe_read_kernel_str(data.name, sizeof(data.name), kstrct->kobj.name);
        bpf_probe_read_kernel_str(data.path, sizeof(data.path), kstrct->parent->kobj.name);
        bpf_probe_read_kernel_str(data.type, sizeof(data.type), kstrct->parent->type->name);

        events.perf_submit(ctx, &data, sizeof(data));

        return 0;
}
