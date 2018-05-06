import socket
import base64
import pprint
import ip_lookup

# variables defining the IP service's host & port
HOST = "localhost"
PORT = 10001


def give_ip_data():
    # start up socket connection
    print("IP service: Initializing socket connection...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("IP service: Binding socket.")
    s.bind((HOST, PORT))
    print("IP service: Listening for connections...")
    s.listen()
    global conn
    conn, addr = s.accept()
    print("IP service: Accepted connection")
    print("IP service: Receiving data...")
    data = conn.recv(1024)
    print("IP service: Received: ")
    print(data)
    ip = base64.b64decode(data).decode("utf-8")
    print("IP Service: Decoded to: ")
    print(ip)
    print("IP service: Looking up IP data...")
    info = str.encode(str(ip_lookup.lookup_ip_info(ip)))
    # send info back to php script
    bool = base64.b64encode(info)
    print("IP service: Sending IP data back to browser...")
    conn.sendall(bool)
    return True
    # restart IP service after this


def main():
    bool = give_ip_data()
    return bool


if __name__ == "__main__":
    main()