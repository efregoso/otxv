from cabby import create_client
import json
import io

# method for retrieving OTX pulses & placing them into the cache file
# UNFINISHED - currently developing

# API Key used for logging in -- BETA VERSION. still altering for custom credentials
OTX_API_KEY = "de0e60ea625d2b840e464f5d44299fcd513a3da48d2d7dd8c3214474dc6dbadb"
# OTX password -- currently set to "password"
OTX_PASSWORD = "password"
# buffer object for pulses
pulses = []

def main():
    # set up the OTX feed as a TAXII client
    client = create_client('otx.alienvault.com', use_https=True, discovery_path='/taxii/discovery')

    # basic authentication -- password ignored in favor of full API key
    # IN PROGRESS
    # client.set_auth(username=OTX_API_KEY, password=OTX_PASSWORD)

    # create a cache stream to a text file to test
    f = open("testcache.txt", "w")

    # pull services from OTX
    services = client.discover_services()

    # write the service names to the cache
    # IN PROGRESS - currently writes to cache the services available
    for service in services:
        f.write('Service type={s.type}, address={s.address}'.format(s=service))
    # otx_get(f)

    # exits the program
    print("System done.")
    exit()

if __name__ == '__main__':
    main()

