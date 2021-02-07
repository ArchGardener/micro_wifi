# MicroWifi

A utility to allow an ESP32 to automatically connect to different networks without needing to hard code credentials.

If the device is unable to connect to a previous network, it will expose an Access Point with a web interface that 
allows to connect to a new network. 

## Uploading
If you're using the Adafruit MicroPython tool (ampy), you can use `upload.sh` to copy the files for you!
```commandline
pip3 install adafruit-ampy
./upload.sh
```

## Usage
```python
"""
Basic - gimme that wifi already
Access point:
    name: MicroWifi
    password: -
"""
from micro_wifi import MicroWifi

wifi = MicroWifi()
wifi.start()
```


```python
"""
Advanced - I know what I want
"""
from micro_wifi import MicroWifi

AP_NAME = 'MeaningOfLife'
AP_PASSWORD = '42'
wifi = MicroWifi(AP_NAME, AP_PASSWORD)
wifi.start()
```


