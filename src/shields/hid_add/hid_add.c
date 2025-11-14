#include<linux/hid.h>

struct hid_add_t {
      // write down here your custom struct vars 
       u32 pid;
       u16 bus;
       u16 vendor;
       u32 prod;
       u32 vers;
       int type;
       char name[100];
       char phys[100];
       char path[15];
};

BPF_PERF_OUTPUT(events);

int hid_add_observer(struct pt_regs *ctx, struct hid_device *kstrct)
{
        struct hid_add_t data = {};
        
        data.pid = bpf_get_current_pid_tgid();
        data.bus =  kstrct->bus;
        data.vendor = kstrct->vendor;
        data.prod = kstrct->product;
        data.vers = kstrct->version;
        data.type = kstrct->type;

        bpf_probe_read_kernel_str(data.name, sizeof(data.name), kstrct->name);
        bpf_probe_read_kernel_str(data.phys, sizeof(data.phys), kstrct->phys);
        bpf_probe_read_kernel_str(data.path, sizeof(data.path), kstrct->dev.parent->kobj.name);

        events.perf_submit(ctx, &data, sizeof(data));

        return 0;
}
