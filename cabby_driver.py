from cabby import create_client
from stix2elevator import elevate_file
import json
import io

# method for retrieving OTX pulses & placing them into the cache file
# IN PROGRESS - currently developing

# API Key used for logging in -- BETA VERSION. still altering for custom credentials
OTX_API_KEY = "de0e60ea625d2b840e464f5d44299fcd513a3da48d2d7dd8c3214474dc6dbadb"
# OTX password -- currently set to "password"
OTX_PASSWORD = "password"
# buffer object for pulses
pulses = []

def main():
    # set up the OTX feed as a TAXII client
    client = create_client('otx.alienvault.com', use_https=True, discovery_path='/taxii/discovery')

    # IN PROGRESS: basic authentication -- password ignored in favor of full API key
    # client.set_auth(username=OTX_API_KEY, password=OTX_PASSWORD)

    # create a cache stream to an XML file to test
    f = open("stix_test.xml", "w")

    # pull services from OTX
    # services = client.discover_services()

    # write the service names to the cache
    # f.write("Services available:\n")
    # for service in services:
    #    f.write('Service type={s.type}, \naddress={s.address}\n'.format(s=service))
    # otx_get(f)

    # write the collections names to the cache
    # f.write("\n\nCollection of user AlienVault:\n")
    collections = client.poll(collection_name="user_AlienVault")
    for collection in collections:
        f.write(collection.content.decode("utf-8"))

    # convert the stix 1.0 to 2.0 json objects & copy to new cache
    # SYSTEM HANGS HERE -- DEBUGGING
    results = elevate_file("stix_test.xml")
    fi = open("testcache2.txt", "w")
    fi.write(results)

    #IN PROGRESS -- extract pulse information from the collections and services
    #   for display in the interface
    # def pulse_get:
    #   in progress

    # exits the program
    print("System done.")
    exit()

if __name__ == '__main__':
    main()

