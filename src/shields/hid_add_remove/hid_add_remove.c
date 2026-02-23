#include <linux/hid.h>
#include <linux/device.h>

#include <kernel_additions_headers.h>

#define MAX_LEN 20

#define HID_ADD_ACT 0
#define HID_REMOVE_ACT 1

struct hid_add_remove_t {
        u32 pid;
        u64 ts;
        u16 bus;
        u16 vendor;
        u32 prod;
        u32 vers;
        int type;
        char name[100];
        char phys[100];
        char path[MAX_LEN];
        char type_remove[MAX_LEN];
        int act_type; 
};

BPF_PERF_OUTPUT(events);

int hid_add_observer(struct pt_regs *ctx, struct hid_device *kstrct)
{
        struct hid_add_remove_t data = {};
        
        data.act_type = HID_ADD_ACT;
        data.pid = bpf_get_current_pid_tgid();
        data.ts = bpf_ktime_get_ns();
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


int hid_remove_observer(struct pt_regs *ctx, struct device *kstrct)
{
        struct hid_add_remove_t data = {};
        
        data.act_type = HID_REMOVE_ACT;
        data.pid = bpf_get_current_pid_tgid();
        bpf_probe_read_kernel_str(data.name, sizeof(data.name), kstrct->kobj.name);
        bpf_probe_read_kernel_str(data.path, sizeof(data.path), kstrct->parent->kobj.name);
        bpf_probe_read_kernel_str(data.type_remove, sizeof(data.type_remove), kstrct->parent->type->name);

        events.perf_submit(ctx, &data, sizeof(data));

        return 0;
}
