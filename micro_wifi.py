import json
from web_server import WebServer
from wifi_manager import WifiManager

ACCESS_POINT_NAME = 'MicroWifi'
ACCESS_POINT_PASSWORD = 'microwifi'


class MicroWifi:
    def __init__(self, ap_name=ACCESS_POINT_NAME, ap_password=ACCESS_POINT_PASSWORD):
        self.web_server = WebServer()
        self.wifi_man = WifiManager(ap_name=ap_name,
                                    ap_password=ap_password)
        # setup web server routes
        self.setup_routes(self.web_server, self.wifi_man)

    def start(self):
        try:
            print('ap starting')
            self.wifi_man.start_ap()
            print('ws starting')
            # start our web server to allow the user to configure the device
            self.web_server.start()
        except Exception as exc:
            print('Error running {}'.format(exc))
        # # try to auto connect
        # self.wifi_man.auto_connect()
        # if self.wifi_man.is_access_point_mode():
        #     # start our web server to allow the user to configure the device
        #     self.web_server.start()

    def stop(self):
        try:
            self.web_server.stop()
        except Exception as exc:
            print('Error stopping {}'.format(exc))

    def setup_routes(self, server, wifi_manager):
        @server.route("/")
        def home(client, request):
            html = ""
            try:
                with open('www/index.html') as f:
                    html = f.read()
            except OSError:
                pass
            server.send_response(client, html)

        @server.route("/scan")
        def scan(client, request):
            networks = wifi_manager.access_point_scan()
            payload = {'networks': networks}
            server.send_response(client, json.dumps(payload), content_type='application/json')

        @server.route("/connect", 'POST')
        def connect(client, request):
            params = server.get_form_data(request)
            ssid = params.get('ssid')
            password = params.get('password')
            # try to connect to the network
            status = wifi_manager.connect(ssid, password)
            payload = {
                'status': status,
                'msg': 'Successfully connected to {}'.format(ssid) if status else 'Error connecting to {}'.format(ssid)
            }
            server.send_response(client, json.dumps(payload), content_type='application/json')
