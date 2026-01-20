#include <kernel_additions_headers.h>

#include <linux/inetdevice.h>
#include <linux/netdevice.h>

#define MAX_LEN 20
#define MAC_ADDR_LEN 6

struct inet_t {
        u32 pid;
        u64 ts;
        int inet_evnt;
        char name[MAX_LEN];
        char mac_addr[MAC_ADDR_LEN];
};
 
static void collect_mac_addr(char *inet_dev, const unsigned char *addr)
{
        int i;
        for (i=0; i < MAC_ADDR_LEN; i++) {
                inet_dev[i] = addr[i];
        }
}

BPF_PERF_OUTPUT(events);

int inet_event_observer(struct pt_regs *ctx, struct notifier_block *kstrct, unsigned long event)
{
        struct inet_t data = {};
        
        data.pid = bpf_get_current_pid_tgid();
        data.ts = bpf_ktime_get_ns();

        // filterting the interesting events related with inet
        if (event == NETDEV_UP || event == NETDEV_DOWN || event == NETDEV_REBOOT || event == NETDEV_CHANGE || event == NETDEV_CHANGENAME) {
                data.inet_evnt = event; 
                events.perf_submit(ctx, &data, sizeof(data));
        }
        

        return 0;
}


int inet_alloc_observer(struct pt_regs *ctx, struct in_device *kstrct)
{
        struct inet_t data = {};
        
        data.pid = bpf_get_current_pid_tgid();
        data.ts = bpf_ktime_get_ns();

        data.inet_evnt = -1;

        bpf_probe_read_kernel_str(data.name, sizeof(data.name), kstrct->dev->name);
        const unsigned char *addr = kstrct->dev->dev_addr;
        unsigned char dev_mac_addr[MAC_ADDR_LEN];
        collect_mac_addr(data.mac_addr, addr);

        events.perf_submit(ctx, &data, sizeof(data));

        return 0;
}

