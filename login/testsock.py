import socket
import base64

HOST = 'localhost'
PORT = 10000

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
print("Received: ")
print(data)
apikey = base64.b64decode(data)
print("Decoded to: ")
print(apikey)
bytes = str.encode("Thank you")
conn.sendall(bytes)
print("Closing socket.")
conn.close()