import socket
import base64
import port_checker
import pprint

# variables defining the Port-checking service's host & port
HOST = "localhost"
PORT = 10002


def check_port():
    # start up socket connection
    print("PC service: Initializing socket connection...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("PC service: Binding socket.")
    s.bind((HOST, PORT))
    print("PC service: Listening for connections...")
    s.listen()
    global conn
    conn, addr = s.accept()
    print("PC service: Accepted connection")
    print("PC service: Receiving data...")
    data = conn.recv(1024)
    print("PC service: Received: ")
    print(data)
    ip = base64.b64decode(data).decode("utf-8")
    print("PC Service: Decoded to: ")
    print(ip)
    print("PC service: Checking IP port...")
    info = str.encode(str(port_checker.check_port(ip)))
    # send info back to php script
    bool = base64.b64encode(info)
    print("PC service: Sending PC result back to browser...")
    conn.sendall(bool)
    return True
    # restart PC service after this


def main():
    bool = check_port()
    return bool


if __name__ == "__main__":
    main()