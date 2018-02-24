from cabby import create_client
import json
import io

def otx_get():


def main():
    # set up the OTX feed as a TAXII client
    client = create_client('https://otx.alienvault.com', discovery_path='/taxii/discovery')

    # basic authentication -- password ignored in favor of full API key
    client.set_auth(username='de0e60ea625d2b840e464f5d44299fcd513a3da48d2d7dd8c3214474dc6dbadb', password='password')

    # create a cache stream to a text file to test
    f = open("testcache.txt", "w")

    # pull in a pulse & write it to the cache
    # IN PROGRESS - currently only write simple Hello.
    f.write("Hello")


    # exits the program
    print("System done.")
    exit()

if __name__ == '__main__':
    main()

