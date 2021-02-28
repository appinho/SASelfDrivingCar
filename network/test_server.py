import socket

HOST = '192.168.0.100'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((HOST, PORT))
s.listen(5)

while True:
	clientsocket, address = s.accept()
	print("Connection from has been established!")
	clientsocket.send(bytes("Welcome", "utf-8"))