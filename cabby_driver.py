import cabby
import json

class cabby_driver(object):

    def __init__(self):
        # set up the OTX feed as a TAXII client
        client = create_client('https://otx.alienvault.com', discovery_path='/taxii/discovery')

        # basic authentication -- password ignored in favor of full API key
        client.set_auth(username='de0e60ea625d2b840e464f5d44299fcd513a3da48d2d7dd8c3214474dc6dbadb', password='password')

        # pull in one pulse to test
