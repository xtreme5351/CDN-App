# Template class for the connection to the car once the device is physically connected
# This is the client, the RPI is the server

import socket

class Connect:
    def start_connection(self):
        print("Connecting")
