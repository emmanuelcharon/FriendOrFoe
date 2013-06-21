#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import semantria
import uuid
import time
import json
import keys

def onRequest(sender, result):
    print("\n", "REQUEST: ", result)


def onResponse(sender, result):
    print("\n", "RESPONSE: ", result)


def onError(sender, result):
    print("\n", "ERROR: ", result)


def onDocsAutoResponse(sender, result):
    print("\n", "AUTORESPONSE: ", len(result), result)


def onCollsAutoResponse(sender, result):
    print("\n", "AUTORESPONSE: ", len(result), result)

def analyze_sentiments(text, semantriaAPIkey, semantriaAPIsecret):
    """ Uses Semantria to analyze the given text. Returns the analysis as a json object. """

    endIndex = min(8000,len(text))
    text = text[0:endIndex]

    serializer = semantria.JsonSerializer()
    session = semantria.Session(semantriaAPIkey, semantriaAPIsecret, serializer, use_compression=True)
    session.Error += onError

   
    sementria_id = str(uuid.uuid1()).replace("-", "")
    doc = {"id": sementria_id, "text": text}
    status = session.queueDocument(doc)
    if status != 202:
        return None

    startTime = time.time()
    while True:
        time.sleep(0.1)	
        status = session.getProcessedDocuments()
        if isinstance(status, list) and len(status)>0:
            return status[0]
        if(time.time()-startTime>3):
            return None

### Example of use
def main():
    text = "I really like Paris. Paris is a beautiful city, full of history and culture. The night life is quite amazing too. I love this city."   
    semantriaAPIkey = keys.semantriaAPIkey
    semantriaAPIsecret = keys.semantriaAPIsecret
    semantria_response = analyze_sentiments(text, semantriaAPIkey, semantriaAPIsecret)
    print(json.dumps(semantria_response, sort_keys=True, indent=4, separators=(',', ': ')))

if __name__ == "__main__":
    main()



    





