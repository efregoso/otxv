from ipwhois import IPWhois
import googlemaps
import warnings
import pprint


'''
Lookup DNS information about a given IP address using the API.

:param ip: An IP address to be looked up for location information
:returns: On successful lookup, will return a dictionary object containing location coordinates. 
On unsuccessful lookup, will return None.
'''
def lookup_ip_info(ip):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        # create a whois instance for the given IP
        whois = IPWhois(ip)
        # create a Google Maps API instance
        gmap = googlemaps.Client('AIzaSyAJYrRExLKqEW794dHT9QuO82aMt2VO3Yg')
        # DEBUG: Add this gmap location to the indicator data
        # This will need to be done from within the ip_lookup.py module.
        # ip_lookup.lookup_qual_ip_info(indicator["indicator"])
        # indicator.update([("qual_location", )])
        # DEBUGGING: print(indicator["location"])
        # lookup the information for this IP and place in a dictionary object
        iplookup = whois.lookup_rdap()
        # need a list here to obtain the first code in the objects dictionary
        keyview = iplookup["objects"].keys()
        itr = list(keyview)
        # continue only if there exist keys
        if len(itr) > 0:
            code = itr[0]
            location = iplookup["objects"][code]["contact"]["address"][0]["value"]
            # DEBUG
            print(location)
            geocode_result = gmap.geocode(location)
            # return the location object only if there is a result from Google Maps
            # send back only if there is a result
            if len(geocode_result) > 0 and geocode_result[0]["geometry"]["location"] is not None:
                # DEBUG: print(pprint.pformat(geocode_result[0]["geometry"]["location"]))
                return geocode_result[0]["geometry"]["location"]
            else:
                return None
        else:
            return None


'''
Lookup DNS information about a given IP address using the whois API & cache to file.

:param ip: An IP address to be looked up for location information
:returns: A boolean on if the location data for the IP was successfully cached
'''
def cache_ip_info(ip):
    # create a whois instance for the given IP
    whois = IPWhois(ip)
    # lookup the information for this IP & place it in ipresults in a "pretty print" format
    # DEBUGGING: maybe try not doing the pretty print to make it bypass the error?
    ipresults = pprint.pformat(whois.lookup_rdap());
    # open a file stream for a demo lookup cache
    lookupf = open("lookup.txt", "w")
    # write the results into the demo lookup cache
    lookupf.write(ipresults)
    return True


if __name__ == '__main__':
    lookup_ip_info('66.99.86.8')
    lookup_ip_info('129.22.21.193')