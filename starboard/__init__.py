import socket


def find_local_free_tcp_port():
    return find_local_free_port(socket.SOCK_STREAM)


def find_local_free_udp_port():
    return find_local_free_port(socket.SOCK_DGRAM)
    
    
def find_local_free_tcp_ports(number):
    return find_local_free_ports(socket.SOCK_STREAM, number)
    
    
def find_local_free_udp_ports(number):
    return find_local_free_ports(socket.SOCK_DGRAM, number)
    

def find_local_free_port(socket_type):
	return find_local_free_ports(socket_type, number=1)[0]


def find_local_free_ports(socket_type, number):
    sockets = []
    try:
        for i in range(0, number):
            s = socket.socket(socket.AF_INET, socket_type)
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
