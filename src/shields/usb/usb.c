#include<linux/usb.h>

#define MAX_LEN 15

struct key_t {
       char path[5];
       u32 pid;
       u64 ts;
       char name[MAX_LEN];
       char serial[MAX_LEN];
       char prod[MAX_LEN];
       char manfc[MAX_LEN];
       char busnam[MAX_LEN];
       int busnum;
};

BPF_PERF_OUTPUT(events);

int usb_observer(struct pt_regs *ctx, struct usb_device *usbd)
{
        struct key_t data = {};
        
        data.pid = bpf_get_current_pid_tgid();
        data.ts = bpf_ktime_get_ns();
        
        bpf_probe_read_kernel_str(data.path, sizeof(data.name), usbd->dev.kobj.name);
       bpf_probe_read_kernel_str(data.name, sizeof(data.name), usbd->dev.type->name);
       bpf_probe_read_kernel_str(data.serial, sizeof(data.serial), usbd->serial);
       bpf_probe_read_kernel_str(data.prod, sizeof(data.prod), usbd->product);
       bpf_probe_read_kernel_str(data.manfc, sizeof(data.manfc), usbd->manufacturer);
       bpf_probe_read_kernel_str(data.busnam, sizeof(data.busnam), usbd->bus->bus_name);
        data.busnum = usbd->bus->busnum;
        
        events.perf_submit(ctx, &data, sizeof(data));

        return 0;
}
