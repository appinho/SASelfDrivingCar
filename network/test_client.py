import socket

HOST = '192.168.0.100'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
buf = 1024
msg = s.recv(buf)
print(msg.decode("utf-8"))
