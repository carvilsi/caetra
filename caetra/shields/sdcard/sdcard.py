#!/usr/bin/env python

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../utils')))

from shields import deploying
from logger_setup import logger
from bcc.utils import printb

SHIELD_NAME="SDCard"

# kernel section
event="mmc_attach_sd"
fn_name="sdcard_observer"
src_file="sdcard.c"

def bpf_main():

    b = deploying.load_bpf_prog(SHIELD_NAME, event, fn_name, src_file)
    
    while 1:
        try:
            (task, pid, cpu, flags, ts, msg) = b.trace_fields()
            logger.info(f"{msg}")
        except ValueError:
            continue
        except KeyboardInterrupt:
            exit()
    
if __name__ == "__main__":
    bpf_main()
