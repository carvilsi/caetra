#include <net/bluetooth/bluetooth.h> 
#include <net/bluetooth/hci.h>
#include <net/bluetooth/hci_core.h>

#define MAX_LEN 20

static void collect_bdaddr(char *dev_bdaddr, bdaddr_t addr)
{
        dev_bdaddr[0] = addr.b[5];
        dev_bdaddr[1] = addr.b[4];
        dev_bdaddr[2] = addr.b[3];
        dev_bdaddr[3] = addr.b[2];
        dev_bdaddr[4] = addr.b[1];
        dev_bdaddr[5] = addr.b[0];
}

struct blt_disconnect_t {
       u32 pid;
       char hci_dev_name[MAX_LEN];
       unsigned char hci_dev_bdaddr[6];
       char name[MAX_LEN];
};

BPF_PERF_OUTPUT(events);

int blt_disconnect_observer(struct pt_regs *ctx, struct hci_dev *kstrct)
{
        struct blt_disconnect_t data = {};
        
        data.pid = bpf_get_current_pid_tgid();
        
        bpf_probe_read_kernel_str(data.hci_dev_name, sizeof(data.hci_dev_name), kstrct->name);
        bpf_probe_read_kernel_str(data.name, sizeof(data.name), kstrct->dev_name);

        bdaddr_t addr = kstrct->bdaddr;
        
        collect_bdaddr(data.hci_dev_bdaddr, addr);

        events.perf_submit(ctx, &data, sizeof(data));

        return 0;
}
