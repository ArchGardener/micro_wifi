#!/bin/bash 

export AMPY_PORT=/dev/ttyUSB0
export AMPY_BAUD=115200

for i in $(find -not -path "./venv/*" -name "*.py" -o -name "*.html"); do # Whitespace-safe but not recursive.
    echo uploading "$i"  
    ampy put "$i" "$i"
done
