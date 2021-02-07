import network


class WifiManager:

    def __init__(self, ap_name='EspAP', ap_password='', ap_max_clients=10, filepath=''):
        self._filepath = filepath
        self._ap_name = ap_name
        self._ap_password = ap_password
        self._ap_max_clients = ap_max_clients
        self.wlan = network.WLAN(network.STA_IF)
        self.ap = network.WLAN(network.AP_IF)
        self._profiles = self._read_profiles()

    def is_access_point_mode(self):
        return self.ap.active()

    def is_wifi_connected(self):
        return self.wlan.active()

    def auto_connect(self):
        # start by scanning all available access points
        self.access_point_scan()

    def start_ap(self):
        # activate the interface
        self.ap.active(True)
        # configure the params 
        self.ap.config(essid=self._ap_name, max_clients=self._ap_max_clients)

    def stop_ap(self):
        # deactivate the interface
        self.ap.active(False)

    def start_wlan(self):
        # activate the interface
        self.wlan.active(True)

    def connect(self, essid='', password=''):
        if self.wlan.isconnected():
            self.disconnect()
        print('connecting to {}'.format(essid))
        self.start_wlan()
        self.wlan.connect(essid, password)
        if self.wlan.isconnected():
            print('connected')
            self._add_new_profile(essid, password)
            self.stop_ap()
            return True
        print('error connecting to {}'.format(essid))
        return False
    
    def disconnect(self):
        print('disconnecting . . .')
        self.wlan.disconnect()

    def access_point_scan(self):
        self.start_wlan()
        # scan and return all available access points
        return self.wlan.scan()

    def _read_profiles(self):
        profiles = {}
        try:
            with open(self._filepath) as f:
                line = f.readline()
                if not line:
                    # EOF
                    return profiles
                ssid, password = line.split(";")
                profiles[ssid] = password
        except OSError:
            pass
        finally:
            return profiles

    def _add_new_profile(self, ssid, password):
        self._profiles = self._read_profiles()
        self._profiles[ssid] = password
        self._write_profiles(self._profiles)

    def _write_profiles(self, profiles):
        with open(self._filepath, "w") as f:
            for ssid, password in profiles.items():
                f.write("{};{}\n".format(ssid, password))
