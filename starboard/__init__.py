import socket


def find_local_free_tcp_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("", 0))
        return s.getsockname()[1]
    finally:
        s.close()


def find_local_free_tcp_ports(number):
    sockets = []
    try:
        for i in range(0, number):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sockets.append(s)
            s.bind(("", 0))
        return [s.getsockname()[1] for s in sockets]
    finally:
        for s in sockets:
            s.close()
        

def find_local_hostname():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    finally:
        s.close()
