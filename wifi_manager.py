import time
import network


class WifiManager:

    AUTH_MODES = {
        0: "open",
        1: "WEP", 
        2: "WPA-PSK", 
        3: "WPA2-PSK", 
        4: "WPA/WPA2-PSK"
    }

    def __init__(self, ap_name='EspAP', ap_password='', filepath='profiles.txt', connection_max_retries=10):
        self._filepath = filepath
        self._ap_name = ap_name
        self._ap_password = ap_password
        self._connection_max_retries = connection_max_retries
        self.wlan = network.WLAN(network.STA_IF)
        self.ap = network.WLAN(network.AP_IF)
        self._profiles = self._read_profiles()

    def is_access_point_mode(self):
        return self.ap.active()

    def is_wifi_connected(self):
        return self.wlan.active()

    def auto_connect(self, include_open=False):
        print('Attempting auto connect')
        if not self._profiles:
            print('No stored profiles, exposing AP')
            self.start_ap()
        connected = False

        # start by scanning all available access points
        print('Scanning for networks')
        networks = self.access_point_scan()
        for ssid, bssid, channel, rssi, authmode, hidden in sorted(networks, key=lambda x: x[3], reverse=True):
            ssid = ssid.decode('utf-8')
            encrypted = authmode > 0
            print("\t Found ssid: %s chan: %d rssi: %d authmode: %s" % (ssid, channel, rssi, self.AUTH_MODES.get(authmode, '?')))
            if not encrypted and include_open:
                # it's not secured so let's try to connect
                connected = self.connect(ssid)
            else:
                if ssid not in self._profiles:
                    # we don't have any profiles for this network so skipping
                    continue
                connected = self.connect(ssid, self._profiles[ssid])
            if connected:
                break
        if not connected:
            print('Failed to detect any previous networks, exposing AP')
            self.start_ap()

    def start_ap(self):
        self.stop_wlan()
        # activate the interface
        self.ap.active(True)
        # configure the params 
        self.ap.config(essid=self._ap_name)

    def stop_ap(self):
        # deactivate the interface
        self.ap.active(False)

    def start_wlan(self):
        # activate the interface
        self.wlan.active(True)

    def stop_wlan(self):
        if self.wlan.isconnected():
            self.wlan.disconnect()
        # deactivate the interface
        self.wlan.active(False)

    def connect(self, essid='', password=''):
        if self.wlan.isconnected():
            self.disconnect()
        print('connecting to {} . . .'.format(essid))
        # switch from ap to wlan mode
        self.start_wlan()
        self.wlan.connect(essid, password)
        # wait a few seconds to see if the connection was successful
        for _ in range(self._connection_max_retries * 2):
            if self.wlan.isconnected():
                break
            time.sleep(0.5)
            print('. . .')
        if not self.wlan.isconnected():
            print('error connecting to {}'.format(essid))
            # enable ap again
            self.start_ap()
            return False
        print('connected')
        self._add_new_profile(essid, password)
        return True

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
        try:
            self._profiles = self._read_profiles()
            self._profiles[ssid] = password
            self._write_profiles(self._profiles)
        except Exception as exc:
            print('Error adding new profile {}'.format(exc))

    def _write_profiles(self, profiles):
        try:
            print('Writing profiles', profiles)
            with open(self._filepath, "w") as f:
                for ssid, password in profiles.items():
                    f.write("{};{}\n".format(ssid, password))
            print('Profile writing completed')
        except Exception as exc:
            print('Error writing profiles {}'.format(exc))
