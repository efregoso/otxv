README.MD - OTX-V
Author: Elizabeth Fregoso

A log for changes made as OTX-V is developed.

3/2/2018

    Started trying to use taxii2-client instead of Cabby to see if I get better results.

    Have abandoned taxii2-client for OXTv2 library.  It looks like this delivers JSON objects
    in STIX 2.0, instead of trying to force Cabby to give me information.

    Successfully am able to import pulse indicator information with OTXv2.  Working on getting
    this information into Kibana & ElasticSearch.

    Have successfully transported IP lookup data from who.is to the module.
    IP Lookup tool is in the works.


------------------------------------------------------------------------------------------

2/23/2018

    Made progress on the cabby_driver.py file.  Have set up essentials for writing to a cache file.
    Still working on modifying Cabby to deliver pulses from OTX to the cache file.

    Pulls both services & collections into the cache.  Still working on extracting pulse information.

    Large breakthrough.  TAXII uses STIX markup language for its CTI objects.  OTX has not updated its
    information storage protocol & stores & sends everything in STIX 1.0, an outdated version.
    This is presumably why I've had so much trouble trying to extract pulse information from the raw files.
    The STIX files now require a conversion "elevator" in order to be read within the cabby driver.
    I was not anticipating this and am upset that it ate up so much time.  At the very least,
    I now know why I've struggled to extract the data from the raw server data I'e been downloading.
    I also do not anticipate STIX will take very long to learn, as it's just abstracted XML.
    I will be patching this up over the weekend.

------------------------------------------------------------------------------------------

2/20/2018

	Added HTML & CSS to the software stack.  Started coding the login page.  Working
	on integrating Cabby into the login page & taking the credentials.  