# MicroWifi
A simple class to assist in wifi for micropython.

**Note: some testing required, milage may vary.**

## Usage
```python
# basic - scan and print all available networks
from micro_wifi import MicroWifi

wifi = MicroWifi()
wifi.auto_start()
```

```python
# gimme an access point
from micro_wifi import MicroWifi

wifi = MicroWifi('')
wifi.start_ap()
```

```python
# just connect already
from micro_wifi import MicroWifi

wifi = MicroWifi()
wifi.connect('essid', 'password')
```
