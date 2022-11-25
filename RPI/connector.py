# This is the script that should run as a daemon on the RPI
# In theory, the daemon constantly listens for connections and when one is found, blocks all other
# Should establish a permanent link until client-side termination

import socket

HOST = "169.254.66.159"
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
