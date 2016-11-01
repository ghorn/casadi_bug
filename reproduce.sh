#!/usr/bin/env bash

# exit on errors
set -e

# export function
python bad_cgen.py

# compile function
gcc -Wall -Wextra -Wno-unused-variable -Wno-unused-parameter -Werror test.c -o yolo

# run it
./yolo
