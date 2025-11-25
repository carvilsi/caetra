#include <net/bluetooth/bluetooth.h> 
#include <net/bluetooth/hci.h>
#include <net/bluetooth/hci_core.h>
#include <linux/bpf.h>
#include <linux/ptrace.h>

#define MAX_LEN 20

static void bdaddr_to_string(bdaddr_t *addr, char *str) {
    snprintf(str, MAX_LEN, "%02x:%02x:%02x:%02x:%02x:%02x",
             addr->b[0], addr->b[1], addr->b[2],
             addr->b[3], addr->b[4], addr->b[5]);
}

struct blt_connect_t {
       u32 pid;
       char hci_dev_name[MAX_LEN];
       /*char hci_dev_bdaddr[MAX_LEN];*/
       unsigned char hci_dev_bdaddr[6];
       /*bdaddr_t hci_dev_bdaddr;*/
       char name[MAX_LEN];
       /*char conn_dev_bdaddr[MAX_LEN];*/
       /*bdaddr_t conn_dev_bdaddr;*/
       char conn_dev_class[MAX_LEN];
};

BPF_PERF_OUTPUT(events);

int blt_connect_observer(struct pt_regs *ctx, struct hci_dev *kstrct, void *conn_data, struct sk_buff *skb)
{
        struct blt_connect_t data = {};
        
        data.pid = bpf_get_current_pid_tgid();

        bpf_probe_read_kernel_str(data.hci_dev_name, sizeof(data.hci_dev_name), kstrct->name);
        bpf_probe_read_kernel_str(data.name, sizeof(data.name), kstrct->dev_name);
        /*bpf_probe_read_kernel_str(data.hci_dev_bdaddr, sizeof(data.hci_dev_bdaddr), (void *) kstrct->bdaddr);*/
        /*data.hci_dev_bdaddr = kstrct->bdaddr;*/
        /*data.hci_dev_bdaddr[0] = kstrct->bdaddr;*/
        /*kstrct->bdaddr->data.hci_dev_bdaddr[0];*/
        /*kstrct->bdaddr->data.hci_dev_bdaddr[0];*/
        bdaddr_t *addr = &kstrct->bdaddr;
        /*char *lol;*/
        /*bdaddr_to_string(addr, lol);	*/
        data.hci_dev_bdaddr[0] = addr->b[0];
        data.hci_dev_bdaddr[1] = addr->b[1];
        data.hci_dev_bdaddr[2] = addr->b[2];
        data.hci_dev_bdaddr[3] = addr->b[3];
        data.hci_dev_bdaddr[4] = addr->b[4];
        data.hci_dev_bdaddr[5] = addr->b[5];
        /*bdaddr_to_string(addr, data.hci_dev_bdaddr);	*/
        /*char *str;*/
        /*bpf_snprintf(data.hci_dev_bdaddr, sizeof(data.hci_dev_bdaddr), "%02x:%02x:%02x:%02x:%02x:%02x",addr->b[0]);*/
        /*data.hci_dev_bdaddr[0] = addr;*/
        /*bpf_probe_read_kernel_str(data.hci_dev_bdaddr, sizeof(data.hci_dev_bdaddr), (void *) &kstrct->bdaddr);*/

        struct hci_ev_conn_request *ev = conn_data;
        
        /*bpf_probe_read_kernel_str(data.conn_dev_class, sizeof(data.conn_dev_class), ev->dev_class);*/
        /*bpf_probe_read_kernel_str(data.conn_dev_bdaddr, sizeof(data.conn_dev_bdaddr), ev->bdaddr);*/
        /*data.conn_dev_bdaddr = ev->bdaddr;*/

        events.perf_submit(ctx, &data, sizeof(data));

        return 0;
}
