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

    def route(self, route_path):
        """
        Route decorator to add a route
        """
        def wrapper(handler):
            self.add_route(route_path, handler)
            return handler
        return wrapper

    def add_route(self, route_path, handler):
        """
        Adds a route by supplying a path and handler manually
        """
        if route_path not in self.routes:
            raise Exception("Route {} already exists.".format(route_path))
        self.routes[route_path] = handler

    def get_route_handler(self, request_path):
        """
        Gets the route handler if applicable
        :param request_path     path to be routed
        :return route handler if available else None
        """
        if request_path in self.routes.keys():
            return self.routes.get(request_path)
        return None

    def _handle_request(self, client, request):
        """
        Request handler takes the inbound request and transforms
        """
        handler = self.get_route_handler(request.path)
        if handler is None:
            self._handle_not_found(client, request)
            return
        # update response with associated handler
        handler(client, request)

    def _handle_not_found(self, client, url):
        pass
