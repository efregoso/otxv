import initialize_indicators
from ipwhois import IPWhois

#Lookup DNS information about a given IP address using the ____ API.
def lookup_ip_info(ip):
    #create a whois instance for the given IP
    whois = IPWhois(ip)
    #lookup the information for this IP & place it in ipresults in a "pretty print" format
    ipresults = pprint.pformat(whois.lookup_rdap());
    #open a file stream for a demo lookup cache
    lookupf = open("lookup.txt", "w")
    #write the results into the demo lookup cache
    lookupf.write(ipresults)