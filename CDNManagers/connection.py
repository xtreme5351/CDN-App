# Template class for the connection to the car once the device is physically connected
# This is the client, the RPI is the server

import socket
import fcntl
import struct
from netifaces import AF_INET, ifaddresses


class Connect:
    def __init__(self):
        self.PORT = 65432
        self.protocol = 'eth0'
        self.HOST = ""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.get_rpi_ip()

    def get_rpi_ip(self):
        self.HOST = ifaddresses('en0')[AF_INET]
        print(self.HOST)

    def start_connection(self):
        print("Connecting")
        with self.sock as s:
            s.connect((self.HOST, self.PORT))
            s.sendall(b"Cum")
            data = s.recv(1024)
        print(f"Received {data!r}")


if __name__ == "__main__":
    Connect().start_connection()
