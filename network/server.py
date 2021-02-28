import io
import socket
import struct
from PIL import Image
import matplotlib.pyplot as plt
from parameters import *

server_socket = socket.socket()
server_socket.bind((ip_address, port))
server_socket.listen(0)
print("1")
# Read bytes
connection = server_socket.accept()[0].makefile('rb')
print("2")
try:
    img = None
    while True:
        print("Read")
        image_length = struct.unpack(
            '<L', connection.read(
                struct.calcsize('<L')))[0]
        if not image_length:
            break
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_length))

        image_stream.seek(0)
        image = Image.open(image_stream)

        if img is None:
            img = plt.imshow(image)
        else:
            img.set_data(image)

        plt.pause(0.01)
        plt.draw()

        print("Image is %dx%d" % image.size)
        image.verify()
        print("Image is verified")


finally:
    connection.close()
    server_socket.close()
