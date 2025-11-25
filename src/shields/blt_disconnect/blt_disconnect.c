#include<net/bluetooth/bluetooth.h net/bluetooth/hci.h net/bluetooth/hci_core.h>

struct blt_disconnect_t {
      // write down here your custom struct vars 
       u32 pid;
};

BPF_PERF_OUTPUT(events);

int blt_disconnect_observer(struct pt_regs *ctx, struct hci_dev *kstrct)
{
        struct blt_disconnect_t data = {};
        
        data.pid = bpf_get_current_pid_tgid();

        //bpf_probe_read_kernel_str(data.path, sizeof(data.path), kstrct->something);

        events.perf_submit(ctx, &data, sizeof(data));

        return 0;
}
