import socket
import network


class WebServer:
    """
    A basic web server
    """

    def __init__(self):
        self.ap = network.WLAN(network.AP_IF)
        self.server_socket = None
        self.routes = {}

    def start(self, port=80):
        # an AP is required
        if not self.ap.isconnected():
            raise Exception('Access Point not running')

        # cleanup any previously connected sockets
        self.stop()

        addr = socket.getaddrinfo('0.0.0.0', port)[0][-1]
        self._create_socket(addr)

        print('Listening on: {}'.format(addr))
        print('Connect to http://192.168.4.1')

        client = None
        while True:
            try:
                client, client_addr = self.server_socket.accept()
                print('Client connection from', client_addr)
                client.settimeout(5.0)

                request = b""
                try:
                    while "\r\n\r\n" not in request:
                        request += client.recv(512)
                except OSError:
                    pass

                print("Request: {}".format(request))
                if "HTTP" not in request:  # skip invalid requests
                    print('Invalid request')
                    continue
                # pass to the request handler
                self._handle_request(client, request)
            finally:
                if client:
                    client.close()

    def stop(self):
        if not self.server_socket:
            print('Socket not available')
            return
        self.server_socket.close()
        self.server_socket = None

    def _create_socket(self, addr):
        self.server_socket = socket.socket()
        self.server_socket.bind(addr)
        self.server_socket.listen(1)

    def _handle_request(self, client, request):
        pass
