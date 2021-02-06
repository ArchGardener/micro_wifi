import network
import socket


class WifiManager:

    def __init__(self, ap_name='EspAP', ap_password='', ap_max_clients=10, filepath=''):
        self._filepath = filepath
        self._ap_name = ap_name
        self._ap_password = ap_password
        self._ap_max_clients = ap_max_clients
        self.wlan = network.WLAN(network.STA_IF)
        self.ap = network.WLAN(network.AP_IF)

    def auto_connect(self):
        # start by scanning all available access points
        self._access_point_scan()

    def start_ap(self):
        # activate the interface
        self.ap.activate(True)
        # configure the params 
        self.ap.config(essid=self._ap_name, max_clients=self._ap_max_clients)

    def start_wlan(self):
        # activate the interface
        self.wlan.active(True)

    def connect(self, essid='', password=''):
        if self.wlan.isconnected():
            self.disconnect()
        print('connecting . . .')
        self.wlan.connect(essid, password)
        print('connected!' if self.wlan.isconnected() else 'error connecting')
    
    def disconnect(self):
        print('disconnecting . . .')
        self.wlan.disconnect()

    def _access_point_scan(self):
        self.start_wlan()
        # scan for access points
        for ap in self.wlan.scan():
            print(ap)
