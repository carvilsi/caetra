#include <net/bluetooth/bluetooth.h> 
#include <net/bluetooth/hci.h>
#include <net/bluetooth/hci_core.h>
#include <linux/bpf.h>
#include <linux/ptrace.h>

#include <kernel_additions_headers.h>

#define MAX_LEN 20

struct blt_connect_t {
       u32 pid;
       char hci_dev_name[MAX_LEN];
       unsigned char hci_dev_bdaddr[6];
       char name[MAX_LEN];
       char conn_dev_bdaddr[6];
       char conn_dev_class[3];
};

static void collect_bdaddr(char *dev_bdaddr, bdaddr_t addr)
{
        dev_bdaddr[0] = addr.b[5];
        dev_bdaddr[1] = addr.b[4];
        dev_bdaddr[2] = addr.b[3];
        dev_bdaddr[3] = addr.b[2];
        dev_bdaddr[4] = addr.b[1];
        dev_bdaddr[5] = addr.b[0];
}

BPF_PERF_OUTPUT(events);

int blt_connect_observer(struct pt_regs *ctx, struct hci_dev *kstrct, void *conn_data, struct sk_buff *skb)
{
        struct blt_connect_t data = {};
        
        data.pid = bpf_get_current_pid_tgid();

        bpf_probe_read_kernel_str(data.hci_dev_name, sizeof(data.hci_dev_name), kstrct->name);
        bpf_probe_read_kernel_str(data.name, sizeof(data.name), kstrct->dev_name);

        bdaddr_t addr = kstrct->bdaddr;
        
        collect_bdaddr(data.hci_dev_bdaddr, addr);

        struct hci_ev_conn_request *ev = conn_data;
        bdaddr_t conn_addr = ev->bdaddr;
        collect_bdaddr(data.conn_dev_bdaddr, conn_addr);

        data.conn_dev_class[0] = ev->dev_class[2];
        data.conn_dev_class[1] = ev->dev_class[1];
        data.conn_dev_class[2] = ev->dev_class[0];

        events.perf_submit(ctx, &data, sizeof(data));

        return 0;
}
