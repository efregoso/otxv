README.MD - OTX-V
Author: Elizabeth Fregoso

A log for changes made as OTX-V is developed.


3/25/2018

    What I want to do this time around: Give Kibana the ability to read from the cache;
    dealing with the encoding error; creating list visualization of the index "pulses"
    currently in the index.



------------------------------------------------------------------------------------------

3/24/2018

    What I want to do this time around: fix the error below, import bulk data into
    Kibana, begin working on list visualization

    Looked into the error I got last time.  There is no other way to address it
    than to print the characters that cannot be encoded in the .txt file to some other
    format.  I know very little about encoding in Python, so for now I will just use
    the data as it has been downloaded to the cache up until the error, about 3.7 Gbs
    of STIX2 objects.

    Despite receiving lots of socket timeout errors while indexing pulse objects, lots of
    them have appeared in Kibana's pulse index.  Have created a screenshots folder with a
    screenshot of what the second pulse looks like.  The problem with these incremental IDs
    is that each time the pulse list updates, all pulse IDs will be downshifted.  Because I am
    trying to limit my work to the pulses that do load, this will be a concern for later.
    Now it is just a matter of finding out where in the pulse list the exceptions occur
    (likely at the error listed above), and finding a way to get that data into Kibana & the cache.

    Next steps: Give Kibana the ability to read from the cache; dealing with the encoding error;
    creating list visualization of the index "pulses".

------------------------------------------------------------------------------------------

3/9/2018

    Successfully created a demo pulse index in Elasticsearch/Kibana with demo pulses inside.
    Am now moving a subsection of real-time pulse information into a non-demo index with the idea
    of working up to the entire AlienVault library gradually, to both keep running time
    down while I try out new features and to make the raw data more manageable.

    JSON cache created!  Program hangs on a character error, posted here for personal reference:
    Traceback (most recent call last):
      File "initialize_indicators.py", line 57, in <module>
        main()
      File "initialize_indicators.py", line 32, in main
        cachef.write(pprint.pformat(pulse))
      File "C:\Users\Chrissy\AppData\Local\Programs\Python\Python36\lib\encodings\cp
    1252.py", line 19, in encode
        return codecs.charmap_encode(input,self.errors,encoding_table)[0]
    UnicodeEncodeError: 'charmap' codec can't encode characters in position 208-216:
     character maps to <undefined>

    I don't know what this means, but the process got significantly far before terminating in this,
    so there are some actual pulses loaded into the cache document.

    Next steps: substitute the demo pulse index with an actual pulse index using the JSON cache
    ("bulk" upload, if possible); move on to visualization

------------------------------------------------------------------------------------------

3/3/2018

    Cache now finally works, holding information about indicator objects in all pulses.
    The scheme by which this information is delivered is EXTREMELY roundabout & the time I
    have spent on it shows it: the pulse objects delivered from the server are composed of a list
    of pulse objects, which are dictionaries containing multiple keys, one being "indicators"
    which is itself, a list of indicator objects, each a dictionary object.  Needless to say,
    this took an incredible amount of trial & error.

    But at last, I have found it!  Time to start pushing it into the elasticsearch engine.

------------------------------------------------------------------------------------------

3/2/2018

    Started trying to use taxii2-client instead of Cabby to see if I get better results.

    Have abandoned taxii2-client for OXTv2 library.  It looks like this delivers JSON objects
    in STIX 2.0, instead of trying to force Cabby to give me information.

    Successfully am able to import pulse indicator information with OTXv2.  Working on getting
    this information into Kibana & ElasticSearch.

    Have successfully transported IP lookup data from who.is to the module.
    IP Lookup tool is in the works.
    
    Developed main.html and style.css files for the homepage (HTML/CSS).  In the process of
    integrating php so the program can use the user's custom API key.

	Summary: Started the IP Lookup Tool, finished general layout of homepage & login.php, 
	got indicator info download working with OTXv2, set up ElasticSearch & Kibana, added
	ElasticSearch package to core module
	Next time: Set up IP Lookup Module, get indicator data funnelled into Elastic Search


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