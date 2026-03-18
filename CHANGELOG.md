# Changelog

# [v1.2.0](https://github.com/carvilsi/caetra/releases/tag/v1.2.0) (2026-03-18)

- Added WebCam shield
- improved shield generator:
    - adding debug kprint function to kerlen space c code
    - not mandatory linux header
    - not mandatory struct
    - small fixes and refactor
    - no as default for CanaryToken and TelegramBot sender

# [v1.1.0](https://github.com/carvilsi/caetra/releases/tag/v1.1.0) (2026-03-17)

- Added CD/DVD ROM shield

# [v1.0.2](https://github.com/carvilsi/caetra/releases/tag/v1.0.2) (2026-02-23)

- Fix bug related with bcc adding missing struct bpf_wq to support kernel 6.14.0-37 on 24.04.1-Ubuntu (noble) 

# [v1.0.1](https://github.com/carvilsi/caetra/releases/tag/v1.0.1) (2026-01-20)

- Fix bug related with bcc v0.35.0 (supports up to Linux 6.14), adding missing struct bpf_task_work to support kernel 6.18.5

# [v1.0.0](https://github.com/carvilsi/caetra/releases/tag/v1.0.0) (2025-11-29)

- First release for the **eBPF Hackathon**
- Shields:
    - ambient_light
    - blt_connect
    - blt_disconnect
    - hibernation
    - hid_add_remove
    - hid_interact
    - inet
    - input_event
    - mmc
    - power
    - usb

