from ipwhois import IPWhois
import pprint
import googlemaps

# Lookup DNS information about a given IP address using the API.


def lookup_ip_info(ip):
    # create a whois instance for the given IP
    whois = IPWhois(ip)
    # create a Google Maps API instance
    gmap = googlemaps.Client('AIzaSyAJYrRExLKqEW794dHT9QuO82aMt2VO3Yg')
    # lookup the information for this IP and place in a dictionary object
    iplookup = whois.lookup_rdap()
    # need a list here to obtain the first code in the objects dictionary
    keyview = iplookup["objects"].keys()
    itr = list(keyview)
    # continue only if there exists keys
    if (len(itr) > 0):
        code = itr[0]
        location = iplookup["objects"][code]["contact"]["address"][0]["value"]
        geocode_result = gmap.geocode(location)
        # return the location object only if there is a result from Google Maps
        # send back only if there is a result
        if len(geocode_result) > 0:
            return geocode_result[0]["geometry"]["location"]

if __name__ == '__main__':
    lookup_ip_info('66.99.86.8')
    lookup_ip_info('129.22.21.193')