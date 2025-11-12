#!/bin/bash

echo "follow the rabbit onto the struct ${1} hole"

FILE_NAME="${1}_rabbit_hole.strct"
_struct=$(bpftrace -lv "struct ${1}")

echo "$_struct" >> $FILE_NAME

_subs=$(echo "$_struct" | awk '/struct\s/ { print $2 }')
_subs_uniq=$(echo "$_subs" | uniq)

for _s in $_subs_uniq; do
        if [ "$1" != "$_s" ]; then
                echo "processing ${_s}"
                bpftrace -lv "struct ${_s}" >> $FILE_NAME
        fi
done
