#include<linux/mmc/host.h>

#define MAX_LEN 15

struct mmc_t {
        char dev_name[MAX_LEN];
        char class_name[MAX_LEN];
        char dev_path0[MAX_LEN];
        char dev_path1[MAX_LEN];
        int mmc_type;
        char prod_name[8];
        int mmc_year;
        int mmc_serial;
        int mmc_manfid;
        int mmc_oemid;
};

BPF_PERF_OUTPUT(events);

int sdcard_observer(struct pt_regs *ctx, struct mmc_host *mmch)
{
        struct mmc_t data = {};
        
        bpf_probe_read_kernel_str(data.dev_name, sizeof(data.dev_name), mmch->class_dev.kobj.name);
        bpf_probe_read_kernel_str(data.class_name, sizeof(data.class_name), mmch->class_dev.class->name);
        bpf_probe_read_kernel_str(data.dev_path0, sizeof(data.dev_path0), mmch->parent->kobj.parent->name);
        bpf_probe_read_kernel_str(data.dev_path1, sizeof(data.dev_path1), mmch->parent->kobj.sd->name);
        data.mmc_type = mmch->card->type;
        bpf_probe_read_kernel_str(data.prod_name, sizeof(data.prod_name), mmch->card->cid.prod_name);
        data.mmc_year = mmch->card->cid.year;
        data.mmc_serial = mmch->card->cid.serial;
        data.mmc_manfid = mmch->card->cid.manfid;
        data.mmc_oemid = mmch->card->cid.oemid;
        
        events.perf_submit(ctx, &data, sizeof(data));
        
        return 0;
}

