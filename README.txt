README.MD - OTX-V
Author: Elizabeth Fregoso

A log for changes made as OTX-V is developed.

4/20/2018

    What I want to do this time: Finish user authentication, Finish Kibana plugins, Begin Kibana extra tabs
        development, Address error in script, Implement updating to last saved date
    Stretch goal: Initialize the Malware Timeline & Port checking tabs

    Sockets in PHP & Python are communicating with each other.  Working on the encoding procedure for the API key.

    Am going in now to Kibana source code to edit HTML/CSS files to account for the new tabs.  Will then add
    the Javascript files in the separate instance of ElasticSearch to repo for finalization.



    Completed: PHP/Python socket setup,
    Next time:

------------------------------------------------------------------------------------------

4/20/2018

    What I want to do this time: Begin Kibana extra tabs development, Address error in script above,
        Implement updating to last saved date, Implement "add pulse to collection" feature, Finish user
        authentication
    Stretch goal: Initialize the Malware Timeline & Port checking tabs

    Working on transferring the API key from the PHP program to the Python program with sockets to finish
    the login screen & customize login for users.  For now, Python's socket doesn't seem to accept the
    connection from PHP's socket, and the PHP script does not lead to the proper web page after submit.
    Still working on this.

    In between my last commit & today, another program went in and changed my PATH variable to the
    Jara JRE.  ElasticSearch was not functional for me, and I spent the last three hours troubleshooting.
    Unlucky day.

    I realized that the reason my PHP wasn't working was because I did not have PHP installed.  Very unlucky
    day.  I am in the middle of that right now.  Committing to show my work so far.

    Completed: Login screen HTML/CSS, Testing with PHP & Python for passing user API key between languages,
        Kibana separate tabs plugin in another instance of ElasticSearch
    Next time: Finish user authentication, Finish Kibana plugins, Begin Kibana extra tabs development,
    Address error in script, Implement updating to last saved date


------------------------------------------------------------------------------------------

4/13/2018

    What I want to do this time: Start creating expanded data statistic features, Find how to catch the UserWarning
        in ip_lookup.py, Finish map visualization on indicators that do not have location data
    Stretch goal: Implement updating to last saved date

    Exported Kibana indeces to add to repo.  To speed up user's first install & prevent the program
    from having to remake indexes every time it is run, they will be included with the executable file.\

    Finished map visualization for objects with or with a location.  Indicators without a
    location go now to (0,0).  I will have to fix this later, but for now this works fine for my purposes.
    Have included a screenshot in the folder.

    I receive an error on a pulse that has an IP indicator as shown here, meaning that ipgeocode does not
    receive any location data back from Google Maps:
        Updating indicator with location.
        5750 W. 95th St., Suite 300
        Overland Park
        KS
        66207
        United States
        {'lat': 38.9573517, 'lng': -94.65221939999999}
        Updating indicator with location.
        701 Lee Rd
        Suite 300
        Chesterbrook
        PA
        19087
        United States
        {'lat': 40.0687641, 'lng': -75.4577225}
        Updating indicator with location.
        None
        Traceback (most recent call last):
          File "initialize_indicators.py", line 336, in <module>
            main()
          File "initialize_indicators.py", line 275, in main
            lng = ipgeocode["lng"]
        TypeError: 'NoneType' object is not subscriptable

    I am still looking into this.

    Completed: Finished map visualization, ElasticSearch/Kibana indeces export, Updating location objects
        with or without location, got rid of UserWarnings on ip_lookup.py
    Next time: Address error in script above, Implement updating to last saved date, Implement "add pulse
        to collection" feature, Finish user authentication


------------------------------------------------------------------------------------------


4/6/2018

    What I want to do this time: Finish implementing map visualization, Start on Timeline view
    Stretch goal: Implement updating to last saved date

    Fully updated all pulses with IPv4 & IPv6 address indicators to include location information
    from Google Maps.

    Timeline visualization complete.  Expanded pulse size to 200 to create better
    timelines.  Screenshot of Kibana's native timelines uploaded.

    Am learning about mappings in Elasticsearch in order to map the new location attribute
    to a "geo_point" type so that the program recognizes it.
    Keep receiving this error when updating the mapping:
    C:\Users\super\AppData\Local\Programs\Python\Python36-32\lib\site-packages\ipwhois\net.py:138: UserWarning: allow_permutations has been deprecated and will be removed. It is no longer needed, due to the depreca
    tion of asn_alts, and the addition of the asn_methods argument.
      warn('allow_permutations has been deprecated and will be removed. '
    C:\Users\super\AppData\Local\Programs\Python\Python36-32\lib\site-packages\ipwhois\asn.py:178: UserWarning: IPASN._parse_fields_dns() has been deprecated and will be removed. You should now use IPASN.parse_fiel
    ds_dns().
      warn('IPASN._parse_fields_dns() has been deprecated and will be '
    PUT http://localhost:9200/pulses/pulse/9 [status:400 request:0.023s]
    Traceback (most recent call last):
      File "initialize_indicators.py", line 264, in <module>
        main()
      File "initialize_indicators.py", line 222, in main
        es.index(index="pulses", doc_type="pulse", id=i, body=pulse)
      File "C:\Users\super\AppData\Local\Programs\Python\Python36-32\lib\site-packages\elasticsearch\client\utils.py", line 76, in _wrapped
        return func(*args, params=params, **kwargs)
      File "C:\Users\super\AppData\Local\Programs\Python\Python36-32\lib\site-packages\elasticsearch\client\__init__.py", line 319, in index
        _make_path(index, doc_type, id), params=params, body=body)
      File "C:\Users\super\AppData\Local\Programs\Python\Python36-32\lib\site-packages\elasticsearch\transport.py", line 314, in perform_request
        status, headers_response, data = connection.perform_request(method, url, params, body, headers=headers, ignore=ignore, timeout=timeout)
      File "C:\Users\super\AppData\Local\Programs\Python\Python36-32\lib\site-packages\elasticsearch\connection\http_urllib3.py", line 180, in perform_request
        self._raise_error(response.status, raw_data)
      File "C:\Users\super\AppData\Local\Programs\Python\Python36-32\lib\site-packages\elasticsearch\connection\base.py", line 125, in _raise_error
        raise HTTP_EXCEPTIONS.get(status_code, TransportError)(status_code, error_message, additional_info)
    elasticsearch.exceptions.RequestError: TransportError(400, 'mapper_parsing_exception', 'field must be either [lat], [lon] or [geohash]')

    Completed: Timeline visualizations, Location data mapping, Map visualization on indicators
        that have location data (IPv4 & IPv6)
    Next time:  Start creating expanded data statistic features, Find how to catch the UserWarning
        in ip_lookup.py, Finish map visualization on indicators that do not have location data


------------------------------------------------------------------------------------------


3/30/2018

    What I want to do this time: Get hits index working, implement list visualization
    Stretch goal: Integrate IP geographic lookup, Implement map visualization

    Socket timeout error is fixed.  All pulses now uploaded to Kibana.  Have amended the
    initialize_indicator.py file to only account for the first ten indexes to
    make the dataset manageable.

    List visualization for pulses finally complete!  Uploaded a screenshot to the screenshots folder.
    Working on adding a field to the indicator objects containing the location of the IP address.

    Added the location field to the indicator objects by updating the pulse dictionary
    before indexing, so location support for indicators of type IPv4 & IPv6 is there.
    Now working with the CAT API to index those locations & display them on a
    geographic map.

    Completed tasks: Implement list visualization, Get hits index working, Integrate IP geographic
        lookup
    Next time: Finish implementing map visualization, Start on Timeline view

------------------------------------------------------------------------------------------


3/25/2018

    What I want to do this time around: Give Kibana the ability to read from the cache;
    dealing with the encoding error; creating list visualization of the index "pulses"
    currently in the index.

    Working from within Kibana now.  The indicators themselves are the pulse hits,
    so I need to amend the way I send data to Kibana inside the program to include only
    the indicators.  The timeline function is being run from the indicators.created index,
    a subindex within pulse objects.

    I need to implement IP lookup sooner than expected because IDS hits do not naturally
    contain any location information on the IP addresses they provide.  I will have to bundle
    this information in with the indicator data somehow.  I am going to make a separate index,
    called "hits", & play around with that instead.

    Have written code for "hits" but no new index in Kibana, even though I have hit the same
    set of exceptions that the pulse index hits despite still adding pulses. Have added
    screenshots of the return error that Kibana gives when trying to access the hit index.

    Have created a pulse index filter in Kibana.  Added a screenshot to the  folder.
    The index isn't isn't entirely functional yet but it will play a big role in
    creating a list visualization.

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

------------------------------------------------------------------------------------------

ON FIRST INSTALL, DOWNLOAD:
    Kibana
    Elasticsearch
    Python
    JDK 8.0
    From PIP: install pandas, OTXv2, elasticsearch

