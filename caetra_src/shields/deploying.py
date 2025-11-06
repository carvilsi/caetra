from bcc import BPF
from logger_setup import logger

# returns a BPF program loaded and attached to kernel
def load_bpf_prog(shield_name, event, fn_name, src_file, description=None):
    if description is not None:
        logger.info(f"\t[ ] {shield_name} shield function: {description}")
    logger.info(f"\t[ ] {shield_name}: loading kernel space src: {src_file}")

    b = BPF(src_file)
    
    logger.info(f"\t[ ] {shield_name}: attaching krpobe \n\t\tevent: {event} \n\t\tfunction: {fn_name}")

    b.attach_kprobe(event, fn_name=fn_name)
    
    logger.info(f"\t[*] {shield_name}: monitoring\n")
    return b
