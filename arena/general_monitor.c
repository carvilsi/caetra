#include<linux/power_supply.h>
#include<linux/usb.h>
#include<linux/of.h>

/*BPF_HASH(power, struct power_supply *);*/
struct key_t {
        unsigned int foo;
        unsigned int bar;
};

/*BPF_HASH(power, int, char);*/
BPF_HASH(power, struct key_t);

int general_monitor(struct pt_regs *ctx)
{
        bpf_trace_printk("general_action");

        return 0;
}

int pwr_monitor(struct pt_regs *ctx, struct power_supply *psy)
{
        struct key_t key;
        key.foo = 0;
        key.bar = 1;

        bpf_trace_printk("%s pwr_actn %d", psy->desc->name, psy->desc->type);
        power.increment(key);

        return 0;
}

int usb_monitor(struct pt_regs *ctx, struct usb_device *usbd)
{
        bpf_trace_printk("|-> %s\n", usbd->dev.kobj.name);

        return 0;
}
