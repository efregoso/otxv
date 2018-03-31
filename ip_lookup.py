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
    # DEBUGGING: pull the location result from the iplookup data
    # print(iplookup["objects"]["ILTN"]["contact"]["address"][0]["value"])
    location = iplookup["objects"]["ILTN"]["contact"]["address"][0]["value"]
    print(location)
    # DEBUGGING: geocode the address found by the iplookup object
    geocode_result = gmap.geocode(location)
    # return the location object
    return geocode_result[0]["geometry"]["location"]
    # DEBUGGING: return the geo_point location of the individual
    # DEBUGGING: open a file stream for a demo lookup cache
    # lookupf = open("lookup.txt", "w")
    # DEBUGGING: write the results into the demo lookup cache
    # lookupf.write(ipresults)

    # DEBUGGING: experimenting with Geobaza -- DID NOT WORK. There is a bug in the source code!
    # query = GeobazaQuery()
    # iplookup = query.get(ip)
    # print(iplookup.geography.center.latitude)
    # print(iplookup.geography.center.longitude)

if __name__ == '__main__':
    lookup_ip_info('66.99.86.8')