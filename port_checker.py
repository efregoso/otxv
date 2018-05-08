# import ping
import pprint


def check_port(ip):
    info = str.encode(str(ping(ip)))
    return info


def main():
    bool = check_port()
    return bool


if __name__ == "__main__":
    main()