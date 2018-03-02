from cabby import create_client
from stix2elevator import elevate_file
from stix2elevator.options import initialize_options
from stix.core import STIXPackage
import datetime
from taxii2client import Server



# method for retrieving OTX pulses & placing them into the cache file
# IN PROGRESS - currently developing

# API Key used for logging in -- BETA VERSION. still altering for custom credentials
OTX_API_KEY = "de0e60ea625d2b840e464f5d44299fcd513a3da48d2d7dd8c3214474dc6dbadb"
# OTX password -- currently set to "password"
OTX_PASSWORD = "password"
# buffer object for pulses
pulses = []
# name of the cache file
cache = 'stixtest.xml'
# name of the plain text cache buffer
buffer = 'testcache.txt'
# name of the cache file with a single package object
stixfrag = 'stixtestfrag.xml'

def main():

    #DEBUGGING -- using the taxii2client instead of cabby.
    server = Server('http://otx.alienvault.com/taxii/discovery', 'emf65', 'password')

    #DEBUGGING -- print server information to console
    print(server.title)

    # set up the OTX feed as a TAXII client
    #client = create_client('otx.alienvault.com', use_https=True, discovery_path='/taxii/discovery')

    # basic authentication -- password ignored in favor of full API key
    # WILL BE CONFIGURED TO ACCEPT CUSTOM LOGIN IN THE FUTURE
    #client.set_auth(username=OTX_API_KEY, password=OTX_PASSWORD)

    # create a cache stream to an XML file to copy the collection contents
    #f = open(cache, "w")

    # DEBUGGING: write the collection content to the cache -- only needed on initialization or update
    #collections = client.poll(collection_name="user_AlienVault")
    #for collection in collections:
    #   xmlvers = STIXPackage.to_xml(collection)
    #   f.write(xmlvers)
    #    f.write(collection.content.decode("utf-8"))

    #EXPERIMENTAL: parse the stix in the XML
    #stix_package = STIXPackage.from_xml(stixfrag);

    #EXPERIMENTAL: dump the data into the testcache
    #fi = open(buffer, "w")
    #fi.write(stix_package)

    # DEBUGGING: convert the stix 1.0 to 2.0 json objects & copy to new cache
    #initialize_options()
    #results = elevate_file("stixtest.xml")
    #fi = open("testcache.txt", "w")
    #fi.write(results)

    # exits the program
    #print("System done.")
    #exit()

def findServices():
    # open a cache file for services
    servf = open("servicesCache.txt", "w")

    # pull services from OTX
    services = client.discover_services()

    # write the service names to the cache
    for service in services:
        f.write('Service type={s.type}, \naddress={s.address}\n'.format(s=service))


#IN PROGRESS -- extract pulse information from the collections and services
#   for display in the interface
# def pulse_get:
#   in progress

if __name__ == '__main__':
    main()

