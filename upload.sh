#!/bin/bash 

export AMPY_PORT=/dev/ttyUSB0
export AMPY_BAUD=115200

for i in $(find . -not -path "./venv/*" -name "*.py" -o -name "*.html"); do # Whitespace-safe but not recursive.
    echo Uploading "$i"  
    ampy put "$i" "$i"
    if [ $? -eq 0 ]; then
        echo ... OK
    else
        echo ... FAILED
        exit
    fi
done

echo rebooting
ampy reset