from ping import verbose_ping
import pprint


def check_port(domain, count):
    fl = float(count)
    # open a file descriptor to stdin
    result = verbose_ping(domain, fl)
    return result


def main():
    bool = check_port()
    return bool


if __name__ == "__main__":
    main()