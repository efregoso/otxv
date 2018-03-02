from stix2elevator import elevate_file
from stix2elevator.options import initialize_options

testfrag = "stixtestfrag.xml"

def main():

    # elevate the file & return into a new file
    initialize_options()
    results = elevate_file(testfrag)
    fi = open("testcache2.json", "w")
    fi.write(results)


if __name__ == '__main__':
    main()