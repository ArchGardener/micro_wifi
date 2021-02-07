import socket
import network
import html


class WebServerRoute:
    def __init__(self, route, method, func):
        self.route = route
        self.method = method
        self.func = func


class WebServer:
    MAX_SOCKET_RECEIVE = 1024

    def __init__(self):
        self.ap = network.WLAN(network.AP_IF)
        self.server_socket = None
        self.routes = {}

    def start(self, port=80):
        # an AP is required
        if not self.ap.active():
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
                        request += client.recv(self.MAX_SOCKET_RECEIVE)
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
            return
        self.server_socket.close()
        self.server_socket = None

    def _create_socket(self, addr):
        self.server_socket = socket.socket()
        self.server_socket.bind(addr)
        self.server_socket.listen(1)

    def route(self, path, method='GET'):
        """
        Route decorator to add a route
        """
        def wrapper(handler):
            self.add_route(path, method, handler)
            return handler
        return wrapper

    def add_route(self, path, method, handler):
        """
        Adds a route by supplying a path, method and handler manually
        """
        route_id = self._make_route_id(path, method)
        if route_id in self.routes:
            raise Exception("Route {} already exists.".format(route_id))
        self.routes[route_id] = WebServerRoute(path, method, handler)

    def get_route_handler(self, request_path, request_method):
        """
        Gets the route handler if applicable
        """
        route_id = self._make_route_id(request_path, request_method)
        if route_id in self.routes.keys():
            return self.routes.get(route_id)
        return None

    def _make_route_id(self, request_path, request_method):
        """
        Creates a route identifier by joining the method to path
        """
        return '{}:{}'.format(request_method, request_path)

    def _handle_request(self, client, request):
        """
        Request handler takes the inbound request and transforms
        """
        # retrieve the request header from the request
        request_header = self.get_request_header(request)
        if not request_header:
            print('Error with request header')
            self._handle_not_found(client, request)
            return
        # split the header to get method/path
        method, path, *_ = request_header.split()
        handler = self.get_route_handler(path, method)
        if handler is None:
            self._handle_not_found(client, request)
            return
        # update response with associated handler
        handler.func(client, request)

    def _handle_not_found(self, client, url):
        error_msg = "Route not found: {}".format(url)
        print(error_msg)
        self.send_response(client, error_msg, status_code=404)

    def send_response(self, client, payload, content_type='text/html', status_code=200):
        try:
            content_length = len(payload)
            self.send_header(client, content_type, status_code, content_length)
            if content_length > 0:
                client.sendall(payload)
        except Exception as exc:
            print('Error sending response {}'.format(exc))
        client.close()

    def send_header(self, client, content_type='text/html', status_code=200, content_length=None):
        try:
            client.sendall("HTTP/1.0 {} OK\r\n".format(status_code))
            client.sendall("Content-Type: {}\r\n".format(content_type))
            if content_length is not None:
                client.sendall("Content-Length: {}\r\n".format(content_length))
            client.sendall("\r\n")
        except Exception as exc:
            print('Error sending header {}'.format(exc))

    def get_request_header(self, request):
        """
        Retrieves the header from a request
        """
        request_data = request.decode().strip().split('\r\n')
        if not request_data:
            return ''
        return request_data[0]

    def get_form_data(self, request):
        res = {}
        request_data = request.decode().strip().split('\r\n')
        if not request_data:
            return res
        for item in request_data[-1].split('&'):
            param = item.split('=', 1)
            if len(param) > 0:
                res[self._unescape(param[0])] = self._unescape(param[1]) if len(param) > 1 else ''
        return res

    def _unescape(self, s):
        """
        Unescapes any html encoded string
        """
        return html.unescape(s.replace('+', ' '))
