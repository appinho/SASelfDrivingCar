import socket

HOST = '192.168.0.100'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

print(HOST)
s.bind((HOST, PORT))
print("bind worked")
s.listen()

clientsocket, address = s.accept()
while True:
    print("Connection from has been established!")
    clientsocket.send(bytes("Welcome", "utf-8"))
