from wifi_manager import WifiManager
from web_server import WebServer

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
        print('ap starting')
        self.wifi_man.start_ap()
        print('ws starting')
        # start our web server to allow the user to configure the device
        self.web_server.start()
        # # try to auto connect
        # self.wifi_man.auto_connect()
        # if self.wifi_man.is_access_point_mode():
        #     # start our web server to allow the user to configure the device
        #     self.web_server.start()

    def stop(self):
        self.web_server.stop()

    def setup_routes(self, server, wifi_manager):
        @server.route("/")
        def home(client, request):
            html = """
            <html><head><title>MicroWifi</title> <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="icon" href="data:,">
            <style></style>
            </head><body>
            <h1>Micro Wifi</h1> 
            </body></html>
            """
            server.send_response(client, html)

        @server.route("/scan")
        def scan(client, request):
            networks = wifi_manager.access_point_scan()
            print(networks)
            payload = {'networks': networks}
            server.send_response(client, payload, content_type='application/json')

        @server.route("/connect", 'POST')
        def connect(client, request):
            # todo - get body from request
            ssid = ''
            password = ''
            # try to connect to the network
            status = wifi_manager.connect(ssid, password)
            payload = {
                'status': status,
                'msg': 'Successfully connected to {}'.format(ssid) if status else 'Error connecting to {}'.format(ssid)}
            server.send_response(client, payload, content_type='application/json')
