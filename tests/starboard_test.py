import threading
import socket

from nose.tools import istest, assert_equals

import starboard


@istest
def can_start_server_on_free_port():
    port = starboard.find_local_free_tcp_port()
    with _start_server(port=port):
        _assert_server_is_running(hostname="localhost", port=port)


@istest
def can_get_multiple_free_ports_at_once():
    port1, port2, port3 = starboard.find_local_free_tcp_ports(number=3)
    
    with _start_server(port=port1):
		with _start_server(port=port2):
			with _start_server(port=port3):
				_assert_server_is_running("localhost", port=port1)
				_assert_server_is_running("localhost", port=port2)
				_assert_server_is_running("localhost", port=port3)


@istest
def can_communicate_with_localhost_using_found_local_hostname():
    hostname = starboard.find_local_hostname()
    port = starboard.find_local_free_tcp_port()
    with _start_server(port=port):
        _assert_server_is_running(hostname=hostname, port=port)


def _start_server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', port))
    sock.listen(1)
    
    class Server(object):
        def __init__(self, sock):
            self._socket = sock
            self._stopped = False
    
        def run(self):
            try:
                while True:
                    connection, client_address = sock.accept()
                    try:
                        connection.recv(1024)
                        connection.sendall("who's there?")
                    finally:
                        connection.close()
            except:
                if not self._stopped:
                    raise
                    
        def __enter__(self):
            return self
            
        def __exit__(self, *args):
            self._stopped = True
            self._socket.shutdown(socket.SHUT_RDWR)
            self._socket.close()
    
    server = Server(sock)
    threading.Thread(target=server.run).start()
    return server
    
def _assert_server_is_running(hostname, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((hostname, port))
        sock.sendall("knock knock")
        data_received = sock.recv(1024)
        assert_equals("who's there?", data_received)
    finally:
        sock.close()
