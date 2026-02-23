#include <kernel_additions_headers.h>

int hibernation_observer(struct pt_regs *ctx)
{
        bpf_trace_printk("lv_hib");

        return 0;
}
