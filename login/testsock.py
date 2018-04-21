import socket

HOST = '172.20.6.85'
PORT = 10001

print("Initializing socket.")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Binding socket.")
s.bind((HOST, PORT))
print("Listening for connections.")
s.listen(10)
conn, addr = s.accept()
print("Accepted connection")
print("Receiving data.")
data = conn.recv(1024)
print("Received:")
print(data)
conn.sendall("Thank you.")
print("Closing socket.")
conn.close()