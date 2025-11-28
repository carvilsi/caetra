#include<linux/power_supply.h>
#include<linux/usb.h>
#include<linux/of.h>
#include<linux/mmc/host.h>
#include<linux/mmc/card.h>
#include<linux/usb.h>
#include<linux/device.h>
#include<linux/hid.h>
#include<linux/input.h>
#include<linux/notifier.h>
#include<linux/backlight.h>
#include <net/bluetooth/bluetooth.h>
#include <net/bluetooth/hci.h>
#include <net/bluetooth/hci_core.h>
#include <linux/bpf.h>
#include <linux/ptrace.h>
/*#include <net/core/dev.h>*/
#include <linux/inetdevice.h>
#include <linux/netdevice.h>

/*#define MMC_TYPE_MMC            0               [> MMC card <]*/
/*#define MMC_TYPE_SD             1               [> SD card <]*/
/*#define MMC_TYPE_SDIO           2               [> SDIO card <]*/
/*#define MMC_TYPE_SD_COMBO       3               [> SD combo (IO+mem) card <]*/
/*#define mmc_card_mmc(c)         ((c)->type == MMC_TYPE_MMC)*/
/*#define mmc_card_sd(c)          ((c)->type == MMC_TYPE_SD)*/
/*#define mmc_card_sdio(c)        ((c)->type == MMC_TYPE_SDIO)*/
/*#define mmc_card_sd_combo(c)    ((c)->type == MMC_TYPE_SD_COMBO)*/
/*int sdcard_observer(struct pt_regs *ctx, struct mmc_host *mmch, struct mmc_card *mmcc)*/

/*#define HCI_MAX_NAME_LENGTH             248*/

int inet_event_monitor(struct pt_regs *ctx, struct notifier_block *kstrct, unsigned long event)
{
        // filter lo (too many triggers)
        /*bpf_trace_printk("0 event |-> %ul", event);*/
        if (event == NETDEV_UP) {
                bpf_trace_printk("NETDEV_UP: %d", event);
        }
        if (event == NETDEV_DOWN) {
                bpf_trace_printk("NETDEV_DOWN: %d", event);
        }
        if (event == NETDEV_REBOOT) {
                bpf_trace_printk("NETDEV_REBOOT: %d", event);
        }
        if (event == NETDEV_CHANGE) {
                bpf_trace_printk("NETDEV_CHANGE: %d", event);
        }
        if (event == NETDEV_CHANGENAME) {
                bpf_trace_printk("NETDEV_CHANGENAME: %d", event);
        }

        return 0;
}

#define MAC_ADDR_LEN 6
 
static void collect_mac_addr(char *inet_dev, const unsigned char *addr)
{
        int i;
        for (i=0; i < MAC_ADDR_LEN; i++) {
                inet_dev[i] = addr[i];
        }
}

int inet_monitor(struct pt_regs *ctx, struct in_device *kstrct)
{
        // filter lo (too many triggers)
        // TODO: filter if name is lo
        bpf_trace_printk("0 name |-> %s", kstrct->dev->name);
        // convert to address
        /*bpf_trace_printk("2 if perm |-> %x", kstrct->dev->perm_addr[0]);*/
        /*bpf_trace_printk("2 if perm |-> %x", kstrct->dev->perm_addr[1]);*/
        /*bpf_trace_printk("3  |-> %s", kstrct->dev->dev_id);*/
        /*bpf_trace_printk("3  |-> %x", kstrct->dev->dev_id);*/
        /*bpf_trace_printk("4  |-> %s", kstrct->dev->dev_port);*/
        /*bpf_trace_printk("4  |-> %x", kstrct->dev->dev_port);*/
        /*bpf_trace_printk("5  |-> %d", kstrct->dev->irq);*/

        /*// same than perm_addr*/
        const unsigned char *addr = kstrct->dev->dev_addr;
        /*bpf_trace_printk("6 addr |-> %s", addr);*/
        /*bpf_trace_printk("6 addr |-> %x", addr);*/
        bpf_trace_printk("6 addr |-> %x", addr[0]);
        bpf_trace_printk("6 addr |-> %x", addr[1]);
        bpf_trace_printk("6 addr |-> %x", addr[2]);
        bpf_trace_printk("6 addr |-> %x", addr[3]);
        bpf_trace_printk("6 addr |-> %x", addr[4]);
        bpf_trace_printk("6 addr |-> %x", addr[5]);

        unsigned char dev_mac_addr[MAC_ADDR_LEN];
        collect_mac_addr(dev_mac_addr, addr);
        bpf_trace_printk("mac addr |-> %s", dev_mac_addr);

        /*bpf_trace_printk("7 broadcast |-> %x", kstrct->dev->broadcast[0]);*/
        /*bpf_trace_printk("7 broadcast |-> %x", kstrct->dev->broadcast[1]);*/

        /*bpf_trace_printk("7 dev name|-> %s", kstrct->dev->dev->name);*/

        /*bpf_trace_printk("6 if perm |-> %x", kstrct->dev->dev_addr[1]);*/
        /*bpf_trace_printk("6 if perm |-> %x", kstrct->dev->dev_addr[2]);*/
        /*bpf_trace_printk("3 if addr |-> %s", kstrct->dev->addr_assign_type);*/
        /*bpf_trace_printk("4 if port |-> %s", kstrct->dev->addr_len);*/
        /*bpf_trace_printk("5 if upper |-> %s", kstrct->dev->upper_level);*/
        /*bpf_trace_printk("6 if lower |-> %s", kstrct->dev->lower_level);*/
        /*struct netdev_name_node name_node = kstrct->dev->name_node;*/
        /*bpf_trace_printk("7 if lower |-> %s", name_node->name);*/

        return 0;
}
 

int bt_connect_monitor(struct pt_regs *ctx, struct hci_dev *kstrct, void *data, struct sk_buff *skb)
{
        bpf_trace_printk("0 name |-> %s", kstrct->name);
        bpf_trace_printk("name |-> %s", kstrct->dev_name);

        struct hci_ev_conn_request *ev = data;
        /*struct hci_ev_conn_complete *ev = data;*/
        bdaddr_t bdc = ev->bdaddr;
        bpf_trace_printk("conn addr |-> %x", bdc.b[5]);
        bpf_trace_printk("conn addr |-> %x", bdc.b[4]);
        bpf_trace_printk("conn addr |-> %x", bdc.b[3]);
        bpf_trace_printk("conn addr |-> %x", bdc.b[2]);
        bpf_trace_printk("conn addr |-> %x", bdc.b[1]);
        bpf_trace_printk("conn addr |-> %x", bdc.b[0]);
        
        
        
        bpf_trace_printk("DEV CLASS |-> %s", ev->dev_class);
        bpf_trace_printk("DEV CLASS |-> %d", ev->dev_class);
        bpf_trace_printk("DEV CLASS |-> %u", ev->dev_class);
        bpf_trace_printk("DEV CLASS |-> %x", ev->dev_class);
        bpf_trace_printk("DEV CLASS |-> %s", ev->dev_class[0]);
        bpf_trace_printk("DEV CLASS |-> %llu", ev->dev_class[0]);
        bpf_trace_printk("DEV CLASS |-> %x", ev->dev_class[0] & 0xffffff);
        bpf_trace_printk("DEV CLASS |-> %x", ev->dev_class[1] & 0xffffff);
        bpf_trace_printk("DEV CLASS |-> %x", ev->dev_class[2] & 0xffffff);


        

        struct hci_event_hdr *hdr = (void *) skb->data;
        bpf_trace_printk("8 event |-> %u", hdr->evt);
        bpf_trace_printk("9 plent |-> %u", hdr->plen);

        bdaddr_t bd = kstrct->bdaddr;

        bpf_trace_printk("dev addr |-> %x", bd.b[5]);
        bpf_trace_printk("dev addr |-> %x", bd.b[4]);
        bpf_trace_printk("dev addr |-> %x", bd.b[3]);
        bpf_trace_printk("dev addr |-> %x", bd.b[2]);
        bpf_trace_printk("dev addr |-> %x", bd.b[1]);
        bpf_trace_printk("dev addr |-> %x", bd.b[0]);

        char blt_dev_addr[6] = { 0 };
        blt_dev_addr[0] = bd.b[5] & 0xffffff;
        blt_dev_addr[1] = bd.b[4] & 0xffffff;
        blt_dev_addr[2] = bd.b[3] & 0xffffff;
        blt_dev_addr[3] = bd.b[2] & 0xffffff;
        blt_dev_addr[4] = bd.b[1] & 0xffffff;
        blt_dev_addr[5] = bd.b[0] & 0xffffff;

        bpf_trace_printk("dev addr gen |-> %x", blt_dev_addr[0]);
        bpf_trace_printk("dev addr gen |-> %x", blt_dev_addr);
        bpf_trace_printk("dev addr gen |-> %s", blt_dev_addr);
        
        
        return 0;
}

int bt_disconnect_monitor(struct pt_regs *ctx, struct hci_dev *kstrct, void *data, struct sk_buff *skb)
{
        bpf_trace_printk("0 name disconn |-> %s", kstrct->name);
        bpf_trace_printk("1 bdaddr disconn |-> %u", kstrct->bdaddr);
        bpf_trace_printk("name |-> %s", kstrct->dev_name);

        struct hci_ev_disconn_complete *ev = data;
        bpf_trace_printk("6 dev class disconn status |-> %x", ev->status);
        bpf_trace_printk("handle disconn |-> %lx", ev->handle);
        bpf_trace_printk("reasson disconn |-> %u", ev->reason);
        

        struct hci_event_hdr *hdr = (void *) skb->data;
        bpf_trace_printk("8 event disconn |-> %u", hdr->evt);
        bpf_trace_printk("9 plent disconn |-> %u", hdr->plen);

        return 0;
}
int light_monitor(struct pt_regs *ctx, struct backlight_device *kstrct)
{
        
        bpf_trace_printk("0|-> %s", kstrct->dev.kobj.name);
        // 1 and 2 are the same
        bpf_trace_printk("1 brightness |-> %d", kstrct->props.brightness);
        /*bpf_trace_printk("2|-> %d", arg1);*/
        bpf_trace_printk("3 power |-> %d", kstrct->props.power);
        bpf_trace_printk("4 type |-> %d", kstrct->props.type);

        return 0;
}

int input_monitor(struct pt_regs *ctx, struct input_dev *kstrct, int arg1, int arg2, int arg3)
{
        
        bpf_trace_printk("0|-> %s", kstrct->dev.kobj.name);
        bpf_trace_printk("4|-> %s", kstrct->name);
        bpf_trace_printk("1|-> %d", arg1);
        bpf_trace_printk("2|-> %d", arg2);
        bpf_trace_printk("3|-> %d", arg3);
        bpf_trace_printk("5|-> %s", kstrct->phys);
        /*bpf_trace_printk("7|-> %d", kstrct->id.product);*/
        /*bpf_trace_printk("8|-> %d", kstrct->id.vendor);*/
        /*bpf_trace_printk("9|-> %s", kstrct->dev.type->name);*/
        /*bpf_trace_printk("6|-> %s", kstrct->uniq);*/

        return 0;
}


int sdcard_observer(struct pt_regs *ctx, struct mmc_host *mmch)
{
        // get name of device
        bpf_trace_printk("%d|-> %s", 0, mmch->class_dev.kobj.name);
        bpf_trace_printk("%d|-> %s", 1, mmch->class_dev.kobj.parent->name);
        bpf_trace_printk("%d|-> %s", 2, mmch->class_dev.kobj.sd->name);
        bpf_trace_printk("%d|-> %s", 3, mmch->parent->kobj.sd->name);
        bpf_trace_printk("%d|-> %s", 4, mmch->parent->kobj.name);
        bpf_trace_printk("%d|-> %s", 5, mmch->parent->kobj.parent->name);
        
        /*int i = mmc_card_mmc(mmch->card); */
        bpf_trace_printk("%d|-> %d", 6, mmch->card->type);

        char *mmc_types[] = {"SD", "MD"};
        char *mtyp = mmc_types[0];
        bpf_trace_printk("%d|-> %s", 76, mtyp);
        if (mmch->card->type == MMC_TYPE_SD) 
                bpf_trace_printk("%d|-> SD", 77);


        bpf_trace_printk("%d|-> %s", 7, mmch->card->scr.sda_vsn);
        bpf_trace_printk("%d|-> %s", 8, mmch->card->scr.sda_spec3);
        bpf_trace_printk("%d|-> %s", 9, mmch->card->info);

        /*unsigned int            manfid;*/
        /*char                    prod_name[8];*/
        /*unsigned char           prv;*/
        /*unsigned int            serial;*/
        /*unsigned short          oemid;*/
        /*unsigned short          year;*/
        /*unsigned char           hwrev;*/
        /*unsigned char           fwrev;*/
        /*unsigned char           month;*/

        /*bpf_trace_printk("%d|-> %p", 100, mmch->card->cid);*/
        bpf_trace_printk("%d|-> %s", 10, mmch->card->cid.prod_name);
        bpf_trace_printk("%d|-> %s", 11, mmch->card->cid.prv);
        bpf_trace_printk("%d|-> %s", 12, mmch->card->cid.hwrev);
        bpf_trace_printk("%d|-> %s", 13, mmch->card->cid.fwrev);
        bpf_trace_printk("%d|-> %s", 14, mmch->card->cid.month);
        bpf_trace_printk("%d|-> %d", 15, mmch->card->cid.year);
        bpf_trace_printk("%d|-> %d", 16, mmch->card->cid.serial);
        bpf_trace_printk("%d|-> %d", 17, mmch->card->cid.manfid);
        bpf_trace_printk("%d|-> %d", 18, mmch->card->cid.oemid);
        
        bpf_trace_printk("%d|-> %s", 19, mmch->card->csd.structure);
        bpf_trace_printk("%d|-> %s", 20, mmch->card->csd.mmca_vsn);
        
        bpf_trace_printk("%d|-> %u", 21, mmch->card->cis.vendor);
        bpf_trace_printk("%d|-> %u", 22, mmch->card->cis.device);
        bpf_trace_printk("%d|-> %u", 23, mmch->card->cis.blksize);
        bpf_trace_printk("%d|-> %u", 24, mmch->card->cis.max_dtr);
        
        


        

        /*char *name = dev_bus_name(&mmch->class_dev);*/
        /*bpf_trace_printk("%d|-> %s", 10, name);*/
        /*int i = dev_is_removable(&mmch->class_dev);*/
        /*bpf_trace_printk("%d|-> %d", 10, i);*/
        /*bpf_trace_printk("%d|-> %d", 6, mmc_card_mmc(mmch->card));*/


        
        /*bpf_trace_printk("%d|-> %s", 6, mmch->ios.chip_select);*/
        /*bpf_trace_printk("%d|-> %s", 7, mmch->class_dev.type->name);*/
        /*bpf_trace_printk("%d|-> %s", 8, mmch->parent->type->name);*/
        /*bpf_trace_printk("%d|-> %s", 9, mmch->class_dev.bus->dev_name);*/
        /*bpf_trace_printk("%d|-> %s", 10, mmch->ios.bus_mode);*/
        /*bpf_trace_printk("%d|-> %s", 11, mmch->card->dev.type->name);*/
        /*bpf_trace_printk("%d|-> %s", 12, mmch->card->dev.kobj.name);*/
        /*bpf_trace_printk("%d|-> %s", 13, mmch->card->host->class_dev.type->name);*/
        /*bpf_trace_printk("%d|-> %s", 14, mmch->card->info);*/
        /*bpf_trace_printk("%d|-> %u", 15, mmch->card->cis.vendor);*/
        /*bpf_trace_printk("%d|-> %d", 16, mmch->card->cis.vendor);*/
        /*bpf_trace_printk("%d|-> %p", 17, mmch->card->cis.vendor);*/
        /*bpf_trace_printk("%d|-> %x", 18, mmch->card->cis.vendor);*/
        /*bpf_trace_printk("%d|-> %d", 19, mmch->card->cis.device);*/
        /*bpf_trace_printk("%d|-> %u", 20, mmch->card->cis.device);*/
        /*bpf_trace_printk("%d|-> %p", 21, mmch->card->cis.device);*/
        /*bpf_trace_printk("%d|-> %x", 22, mmch->card->cis.device);*/
        /*bpf_trace_printk("|-> %s", mmcc->dev.type->name);*/
        /*bpf_trace_printk("|-> %s", mmcc->info);*/
        /*bpf_trace_printk("|-> %u", mmcc->cis.vendor);*/
        /*bpf_trace_printk("|-> %u", mmcc->cis.device);*/

        return 0;
}
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

int hibernation_monitor(struct pt_regs *ctx, struct notifier_block *kstrct)
{

        /*bpf_trace_printk("0 hibernation|-> %s", kstrct->desc->name);*/
        bpf_trace_printk("0 hibernation|->");
 
        return 0;
}


int pwr_monitor(struct pt_regs *ctx, struct power_supply *kstrct)
{

        bpf_trace_printk("0 powe_supply|-> %s", kstrct->desc->name);
        bpf_trace_printk("1 powe_supply|-> %d", kstrct->desc->type);
        /*bpf_trace_printk("2 powe_supply|-> %s", kstrct->supplied_to);*/
        /*bpf_trace_printk("3 powe_supply|-> %s", kstrct->supplied_from);*/
        /*bpf_trace_printk("4 powe_supply|-> %d", kstrct->changed);*/
 
        return 0;
}

int usb_monitor(struct pt_regs *ctx, struct usb_device *usbd)
{
        bpf_trace_printk("0 usb_notify_add_device|-> %s\n", usbd->dev.type->name);
        bpf_trace_printk("0.0 usb_notify_add_device|-> %s\n", usbd->parent->dev.type->name);
        bpf_trace_printk("0.0 usb_notify_add_device|-> %s\n", usbd->dev.parent->type->name);
        bpf_trace_printk("1 usb_notify_add_device|-> %s\n", usbd->serial);
        bpf_trace_printk("2 usb_notify_add_device|-> %s\n", usbd->product);
        bpf_trace_printk("3 usb_notify_add_device|-> %s\n", usbd->manufacturer);
        bpf_trace_printk("4 usb_notify_add_device|-> %s\n", usbd->bus->bus_name);
        bpf_trace_printk("5 usb_notify_add_device|-> %d\n", usbd->bus->busnum);
        bpf_trace_printk("6 usb_notify_add_device|-> %x\n", usbd->descriptor.bDeviceClass);
        /*bpf_trace_printk("6|-> %d\n", usbd->bus->root_hub->serial);*/
        /*bpf_trace_printk("4|-> %s\n", usbd->dev.init_name);*/
        /*bpf_trace_printk("6 hid_device_remove|-> %s\n",  usbd->dev.physical_location->panel);*/
        /*bpf_trace_printk("7 hid_device_remove|-> %s\n",  usbd->dev.physical_location->vertical_position);*/
        /*bpf_trace_printk("8 hid_device_remove|-> %s\n",  usbd->dev.physical_location->horizontal_position);*/
        /*bpf_trace_printk("9 hid_device_remove|-> %u\n",  usbd->dev.physical_location->dock);*/
        /*bpf_trace_printk("10 hid_device_remove|-> %u\n", usbd->dev.physical_location->lid);*/
   

        return 0;
}


/*enum hid_type {*/
  /*HID_TYPE_OTHER = 0,*/
  /*HID_TYPE_USBMOUSE,*/
  /*HID_TYPE_USBNONE*/
/*};*/

int hid_monitor(struct pt_regs *ctx, struct hid_device *hidd)
{
        /*bpf_trace_printk("1 hid_add_device|-> %u\n", hidd->group);*/
        bpf_trace_printk("0 hid_add_device|-> %u\n", hidd->bus);
        bpf_trace_printk("2 hid_add_device|-> %u\n", hidd->vendor);
        bpf_trace_printk("3 hid_add_device|-> %u\n", hidd->product);
        bpf_trace_printk("4 hid_add_device|-> %u\n", hidd->version);
        bpf_trace_printk("5 hid_add_device|-> %d\n", hidd->type);
        bpf_trace_printk("6 hid_add_device|-> %s\n", hidd->name);
        bpf_trace_printk("7 hid_add_device|-> %s\n", hidd->phys);
        bpf_trace_printk("12 hid_add_device|-> %s\n",hidd->dev.parent->kobj.name);

        char comm[TASK_COMM_LEN];
        bpf_get_current_comm(&comm, sizeof(comm));
        bpf_trace_printk("13 hid_add_device|-> %s\n", comm);
        /*bpf_trace_printk("8 hid_add_device|-> %s\n", hidd->uniq);*/
        /*if (hidd->battery != NULL)*/
                /*bpf_trace_printk("9 hid_add_device|-> %d\n", hidd->battery_capacity);*/
        /*bpf_trace_printk("10 hid_add_device|-> %d\n", hidd->country);*/
        /*bpf_trace_printk("10 hid_add_device|-> %p\n", hidd->bpf);*/
        /*bpf_trace_printk("11 hid_add_device|-> %s\n", hidd->driver->name);*/
        
        /*bpf_trace_printk("11 hid_add_device|-> %s\n", hidd->dev.kobj.name);*/
        /*possible to de-authorize*/
        /*bpf_trace_printk("13 hid_add_device|-> %s\n", hidd->dev.init_name);*/
        /*bpf_trace_printk("14 hid_add_device|-> %s\n", hidd->dev.type->name);*/
        /*bpf_trace_printk("15 hid_add_device|-> %s\n", hidd->dev.removable);*/
        /*bpf_trace_printk("16 hid_add_device|-> %s\n", hidd->dev.physical_location->panel);*/
        /*bpf_trace_printk("17 hid_add_device|-> %s\n", hidd->dev.physical_location->vertical_position);*/
        /*bpf_trace_printk("18 hid_add_device|-> %s\n", hidd->dev.physical_location->horizontal_position);*/
        /*bpf_trace_printk("19 hid_add_device|-> %u\n", hidd->dev.physical_location->dock);*/
        /*bpf_trace_printk("20 hid_add_device|-> %u\n", hidd->dev.physical_location->lid);*/
   


        return 0;
}

int hid_monitor_remove(struct pt_regs *ctx, struct device *dev)
{
        bpf_trace_printk("0 hid_device_remove|-> %s\n", dev->kobj.name);
        bpf_trace_printk("1 hid_device_remove|-> %s\n", dev->parent->kobj.name);
        /*bpf_trace_printk("2 hid_device_remove|-> %s\n", dev->init_name);*/
        /*bpf_trace_printk("2.2 hid_device_remove|-> %s\n", dev->parent->init_name);*/
        /*bpf_trace_printk("3 hid_device_remove|-> %s\n", dev->type->name);*/
        /*this one interesting*/
        bpf_trace_printk("3.3 hid_device_remove|-> %s\n", dev->parent->type->name);
        /*bpf_trace_printk("4 hid_device_remove|-> %s\n", dev->removable);*/
        /*bpf_trace_printk("4.4 hid_device_remove|-> %s\n", dev->parent->removable);*/
        /*bpf_trace_printk("5 hid_device_remove|-> %s\n", dev->physical_location->panel);*/
        /*bpf_trace_printk("6 hid_device_remove|-> %s\n", dev->physical_location->vertical_position);*/
        /*bpf_trace_printk("7 hid_device_remove|-> %s\n", dev->physical_location->horizontal_position);*/
        /*bpf_trace_printk("8 hid_device_remove|-> %u\n", dev->physical_location->dock);*/
        /*bpf_trace_printk("8.8 hid_device_remove|-> %u\n", dev->parent->physical_location->dock);*/
        /*bpf_trace_printk("9 hid_device_remove|-> %x\n", dev->physical_location->lid);*/
   

        return 0;
}
