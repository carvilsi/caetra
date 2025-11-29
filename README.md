<div align="center">
<pre>
       ▗      
▛▘▀▌█▌▜▘▛▘▀▌
▙▖█▌▙▖▐▖▌ █▌
Linux Physical Security based on eBPF
When eBPF met CanaryTokens
</pre>
</div>

# Caetra

Caetra ([/kaˈetɾa/](https://ipa-reader.com/?text=ka%CB%88et%C9%BEa&voice=Conchita)) was the [shield used by Iberian](https://en.wikipedia.org/wiki/Caetra)

Caetra uses [eBPF](https://ebpf.io/) (**extended Berkeley Packet Filters**) to try secure a Linux machine against **physical threats**, like implants installation or badUSB usage, or at least be aware about a potential attack, monitoring kernel *kprobes* related with hardware interactions like **attaching an USB**, **detaching an HID** or **uplug** the laptop from **power source**. It uses **BPF Compiler Collection** [BCC](https://github.com/iovisor/bcc/) to do the **kernel tracing** and **manipulation program**.

In order to be able to **notify the user or cybersecurity responsables** by now **Caetra** uses [Thinkst Canary](https://canary.tools/#why) and/or [Telegram Bot](https://core.telegram.org/bots/api). On the other hand a more defensive approach has been implemented on *USB Shield* that allows to [de-authorize](https://www.kernel.org/doc/html/v5.15/usb/authorization.html) the attached device.



--- 

## TOC

1. [Install](#install)
    1. [Dependencies](#dependencies")
2. [Run](#run)
3. [Shields](#shields)
    1.  [ambient_light](#ambient_light)
    2.  [blt_connect](#blt_connect)
    3.  [blt_disconnect](#blt_disconnect)
    4.  [hibernation](#hibernation)
    5.  [hid_add_remove](#hid_add_remove)
    6.  [hid_interact](#hid_interact)
    7.  [inet](#inet)
    8.  [input_event](#input_event)
    9.  [mmc](#mmc)
    10. [power](#power)
    11. [usb](#usb)
4. [Senders](#senders)
    1. [CanaryTokens](#canarytokens)
    2. [Telegram](#telegram)
6. [Logging](#logging)
7. [Project Structure](#project-structure)
    1. [Configuration](#configuration)
    2. [Shields Config](#shields-config)
8. [Tools](#tools)
9. [Notes](#notes)
    1. [TODOS](#todos)
        1. [Shields TODOS](#shields-todos)
        2. [Code](#code)
        3. [Senders TODOS](#senders-todos)

---

## Install<a name="install" />

`$ git clone https://github.com/carvilsi/caetra'`

`$ cd caetra`

Check next [Dependencies section](#dependencies).

### Dependencies<a name="dependencies" />

- Python vers >= 3.12

- [bcc](https://github.com/iovisor/bcc/blob/b63d7e38e8a0f6339fbd57f3a1ae7297e1993d92/INSTALL.md)

## Run<a name="run" />

Right now **eBPF** requires to be execute as **root**.

`sudo ./caetra.py`

## Shields<a name="shields" />

Shields are the *eBPF* programs that monitors the physical interaction with the equip.

Consists on kernel space code in c and user space script in python.

Right now all the Shields are based on [kprobes](https://github.com/iovisor/bcc/blob/b63d7e38e8a0f6339fbd57f3a1ae7297e1993d92/docs/reference_guide.md#1-kprobes)

Current implemented **Caetra's Shields**:

### ambient_light<a name="ambient_light" />

Shield that triggers notification when the **backlight** of screen changes.

This could means that someone aproached to your machine.

**kprobe:** `backlight_device_set_brightness`

### blt_connect<a name="blt_connect" />

This shields triggers when a **Bluetooth** device connects or tries to connect or bind to your machine.

**kprobe:** `hci_conn_request_evt`

### blt_disconnect<a name="blt_disconnect" />

Triggers when a **Bluetooth** device has been disconected from the machine.

**kprobe:** `hci_disconn_complete_evt`

### hibernation<a name="hibernation" />

This Shield will trigger when the machine goes out from **hibernation** mode.

**kprobe:** `unregister_pm_notifier`

### hid_add_remove<a name="hid_add_remove" />

Triggers when an **HID device** has been deatached from your machine. 

Here we are thinking about a possible keyboad **implant** e.g. a [keylogger](https://github.com/therealdreg/okhi)

**kprobe:** `hid_add_device`

**kprobe:** `hid_device_remove`

### hid_interact<a name="hid_interact" />

This Shield triggers when there is a **HID interaction**; the mouse has been moved or a key from external keyboard has been pressed.

**kprobe:** `hid_report_raw_event`

### inet<a name="inet" />

Triggers when there is changes on networking for **inet device**

**kprobe:** `inet_alloc_ifa`

**kprobe:** `inetdev_event`

### input_event<a name="input_event" />

Shield that triggers when there is any input interaction, e.g. trackpad, touchscreen, keyboard, etc...

**kprobe:** `input_handle_event`

### mmc<a name="mmc" />

The Shield reacts when a **MMC** (MultiMediaCard) is inserted. e.g. SDCard.


**kprobe:** `mmc_sd_runtime_suspend`

### power<a name="power" />

Triggers when the **power** source changes.

Thinking that someone has been disconnected the laptop from power plug, e.g. to access hardware parts to perform a [phiysical RAM memory dump](https://docs.buspirate.com/docs/overview/ddr-ram-i2c-adapter/). (

**kprobe:** `power_supply_changed`

### usb<a name="usb" />

This Shield reacts when an **USB** has been connected to the machine.

We are thinking here about a **badUSB** or data exfiltration from the equip. (same idea than [CanaryUSB](https://github.com/carvilsi/canaryusb))

This Shields can **de-authorize** the USB device, via configuration.


**kprobe:** `usb_notify_add_device`

## Senders<a name="senders" />

What Caetra uses to send you a notification, when any Shield has been trigger.

It is possible to configure each shield to handle custom notification for it, via *toml* file under `src/shields/[shield]/[shield.toml]`. e.g. if you want that specific shield to send the notification to a certain Telegram Bot or mail in case of CanaryToken usage. Check an example [here](https://github.com/carvilsi/caetra/blob/main/src/shields/usb/usb.toml#L24)

### CanaryTokens<a name="canarytokens" />

Will send an email with data related with the triggered Shield via DNS Canarytoken powered by [Thinkst Canary](https://canary.tools/).

Get your [DNS Canarytoken](https://docs.canarytokens.org/guide/dns-token.html#what-is-a-dns-canarytoken) and add it to the *token* variable on [general configuration file](https://github.com/carvilsi/caetra/blob/main/config/develop.toml#L14) or [specific shield](https://github.com/carvilsi/caetra/blob/main/src/shields/usb/usb.toml#L28) one. 

### Telegram<a name="telegram" />

Will use [Telegram Bot API]() to send data related with the triggered Shield to the configured **Telegram Chat**.

## Logging<a name="logging" />

Caetra by default will do logging on *logs/* folder with file rotating behaviour. The main logging level could be set on *toml* configuration file with the variable **level** under *logging* [section](https://github.com/carvilsi/caetra/blob/main/config/develop.toml#L9).

The Shields by default will log on **syslog** with **warning** level.

To check the **syslog** Caetra's messages:

`$ journalctl -r --grep='caetra_shields'`

## Project Structure<a name="project-structure" />

### Configuration<a name="configuration" />

### Shields Config<a name="shields-config" />

## Tools<a name="tools" />

## Notes<a name="notes" />

### TODOS<a name="todos" />

#### Shields TODOs<a name="shields-todos" />

- [ ] accelerometers (I don't have a device with an accelerometer sensor)
 
#### Code<a name="code" />

- [ ] cli

#### Senders TODOs<a name="senders-todos" />

- [ ] implement elasticSearch and Kibana
