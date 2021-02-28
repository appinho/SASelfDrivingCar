import io
import socket
import struct
import time
import picamera
from parameters import *

client_socket = socket.socket()

client_socket.connect((ip_address, port))
# Write bytes
connection = client_socket.makefile('wb')
try:
	camera = picamera.Picamera()
	camera.vflip = True
	camera.resolution = (320, 240)
	camera.start_preview()
	time.sleep(2)

	start = time.time()
	stream = io.BytesIO()

	for _ in camera.capture_continuous(stream, 'jpeg'):
		connection.write(struct.pack('<L', stream.tell()))
		connection.flush()

		stream.seek(0)
		connection.write(stream.read())

		# Run the stream for 30 seconds
		if time.time() - start > 30:
			break
		stream.seek(0)
		stream.truncate()

	connection.write(struct.pack('<L', 0))
finally:
	connection.close()
	client_socket.close()