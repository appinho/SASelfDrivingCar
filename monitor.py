import io
import pickle
import socket
import struct
from PIL import Image
import matplotlib.pyplot as plt
from network.parameters import *
from localization import viz
import matplotlib.pyplot as plt

server_socket = socket.socket()
server_socket.bind((ip_address, port))
server_socket.listen(0)
fig, ax = plt.subplots(clear=True)
try:
    while True:
        print("Read")
        conn, addr = server_socket.accept()

        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                best_particle = pickle.loads(data)
                #best_particle = struct.unpack('<3f',data)
                # best_particle.show()
                viz.draw2(fig, ax, "Localization demo", best_particle)
                if not data:
                    break
                conn.sendall(data)

finally:
    # connection.close()
    server_socket.close()
