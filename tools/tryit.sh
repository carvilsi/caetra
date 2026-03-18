#!/bin/bash

# Simple script to test probes faster

bpftrace -e "${1} { printf(\"%s\n\", comm) }"
