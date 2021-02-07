from wifi_manager import WifiManager
from web_server import WebServer

ACCESS_POINT_NAME = 'MicroWifi'
ACCESS_POINT_PASSWORD = 'microwifi'


def main():
    web_server = WebServer()
    wifi_man = WifiManager(ACCESS_POINT_NAME, ACCESS_POINT_PASSWORD)
    # setup web server routes
    setup_routes(web_server, wifi_man)
    # try to auto connect
    wifi_man.auto_connect()

    if wifi_man.is_access_point_mode():
        # start our web server to allow the user to configure the device
        web_server.start()


def setup_routes(app, wifi_manager):

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


if __name__ == '__main__':
    main()