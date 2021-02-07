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
        self.wifi_man.start_ap()
        # start our web server to allow the user to configure the device
        self.web_server.start()

        # # try to auto connect
        # self.wifi_man.auto_connect()
        # if self.wifi_man.is_access_point_mode():
        #     # start our web server to allow the user to configure the device
        #     self.web_server.start()

    def stop(self):
        pass

    def setup_routes(self, app, wifi_manager):
        @app.route("/")
        def home(client, request):
            html = """
            <html><head><title>MicroWifi</title> <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="icon" href="data:,">
            <style></style>
            </head><body>
            <h1>Micro Wifi</h1> 
            </body></html>
            """
            wifi_manager.send_response(client, html)