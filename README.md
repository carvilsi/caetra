# ebpf-physical-sec
Linux Physical Security based on eBPF

## Introduction

Caetra was the shield used by Iberian

## Install

### Dependencies

- Python 3

- [bcc](https://github.com/iovisor/bcc/blob/b63d7e38e8a0f6339fbd57f3a1ae7297e1993d92/INSTALL.md)


## TODOs
- [ ] quite possible that we need to filter events by pid since there are multiple probes that triggers on the same physical interaction. Redis? file?
- [x] maybe it's interesting to add an action label
- [x] added limiting notification for same action
 
### Physical layer AKA Shields
- [ ] bluetooth on connect or pair (arena-wip)
- [ ] bluetooth on disconnect (wip on heynote)
- [x] sdcard attached
- [x] usb attached (also possible to de-auth)
- [x] usb attached add more data
- [ ] ethernet on connect cable
- [ ] accelerometers (I don't have a device with an accelerometer sensor)
- [ ] light sensor (wip arena)
- [x] change on power source
- [x] an usb HID has been disconnected/connected
- [x] try to get more info
- [ ] any keyboard, mouse or tracpad interaction (arena-wip)
- [ ] get out from suspend (arena-wip)
- [ ] get out lock

### code
- [x] sender canary tokens
- [x] sender telegram bot
- [x] configuration file 
- [ ] cli
- [x] reformat splitting to c and py code
- [x] logger; syslog and file
- [x] rotate file logger

### tools
- [x] scafoild

### hackathon
- [ ] readme
- [ ] video

