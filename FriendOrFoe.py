# -*- coding: utf-8 -*-
import diffbot
import semantria_
import mozscape

import json
import sys
import keys

def getAllData(url, mozscapeAPIaccessID, mozscapeAPIkey, diffbotAPIkey, semantriaAPIkey, semantriaAPIsecret):
    
    # Find backlinks using Mozscape
    print "Mozscape is finding backlinks..."
    backlinks = mozscape.get_backlinks(url, mozscapeAPIaccessID, mozscapeAPIkey)

    # Extract data using Diffbot and analyze sentiment using Semantria
    print "Diffbot is extracting backlinks ("+str(len(backlinks))+" backlinks) and Semantria is analyzing the content..."
    reference = diffbot.extract_article(url, diffbotAPIkey)
    if reference["text"]:
        reference["semantria"] = semantria_.analyze_sentiments(reference["text"], semantriaAPIkey, semantriaAPIsecret)
    else:
        return None

    result = list()
    result.append(reference)
    
    for backlink in backlinks:
        data = diffbot.extract_article(backlink, diffbotAPIkey)
        if "text" in data.keys() and data["text"]!=None:
            data["semantria"] = semantria_.analyze_sentiments(data["text"], semantriaAPIkey, semantriaAPIsecret)
            result.append(data)
            
    return result

def analyze(reference, external):
    print("reference url:"+ reference["url"])
    print("backlink url: "+ external["url"])

    
    reference_entities = dict() # entities and scores, plus list of themes and scores
    reference_themes = dict() # 'entity for theme' and scores
    if "semantria" in reference.keys() and reference["semantria"]!=None :
        if "entities" in reference["semantria"].keys() and reference["semantria"]["entities"]!=None :            
            for entity in reference["semantria"]["entities"]:
                reference_entities[entity["title"]] = entity["sentiment_score"]
                if "themes" in entity.keys():
                    for theme in entity["themes"]:
                        reference_themes[entity["title"]+" as "+theme["title"]] = theme["sentiment_score"]
   
    if "semantria" in external.keys() and external["semantria"]!=None :
        if "entities" in external["semantria"].keys() and external["semantria"]["entities"]!=None :
            for entity in external["semantria"]["entities"]:
                if entity["title"] in reference_entities.keys():
                    refScore = reference_entities[entity["title"]]
                    bklScore = entity["sentiment_score"]
                    if (refScore>=0 and bklScore>=0) or (refScore<0 and bklScore<0): 
                        agreeString = "  FRIEND (diff="+str(refScore-bklScore)+")"
                    else:
                        agreeString = "  FOE (diff="+str(refScore-bklScore)+")"
                    print("ENTITY: "+entity["title"] +" (as "+ entity["entity_type"]+")")
                    print(agreeString)
                    print("    reference sentiment score:"+str(refScore))
                    print("    backlink  sentiment score:"+str(bklScore))
                
                if "themes" in entity.keys():
                    for theme in entity["themes"]:
                        refTheme = entity["title"]+" as "+theme["title"]
                        if refTheme in reference_themes.keys(): 
                            refScore = reference_themes[refTheme]
                            bklScore = theme["sentiment_score"]
                            if (refScore>=0 and bklScore>=0) or (refScore<0 and bklScore<0): 
                                agreeString = "  FRIEND (diff="+str(refScore-bklScore)+")"
                            else:
                                agreeString = "  FOE (diff="+str(refScore-bklScore)+")"
                            print("Theme: "+theme["title"]+" (concerning "+ entity["title"]+")")
                            print(agreeString)
                            print("    reference sentiment score:"+str(refScore))
                            print("    backlink  sentiment score:"+str(bklScore))
    print("")
                            

def main(url):
    if len(url)>=7 and "http://"==url[0:7]:
        fetch_example = True
    elif len(url)>=8 and "https://"==url[0:8]:
        fetch_example = True
    elif url in ["allData_example1.json","allData_example2.json","allData_example3.json","allData_example4.json"]:
        fetch_example = False
    else:
        print "Wrong argument: "+url+". Try: allData_example1.json (or 2, or 3)."
        return 
    
    if(fetch_example):
        allData = getAllData(url, keys.mozscapeAPIaccessID, keys.mozscapeAPIkey, keys.diffbotAPIkey, keys.semantriaAPIkey, keys.semantriaAPIsecret)             
        # Save result in allData.json
        with open('allData.json', 'w') as outfile:
            json.dump(allData, outfile, sort_keys=True, indent=3, separators=(',', ': '))
            print "Fetched all data and saved it in allData.json"
    else:
        with open(url, 'r') as infile:
            allData = json.load(infile)
            print "Loaded data from allData.json"

    reference = allData[0]
    
    for i in range(1, len(allData)):
        external = allData[i]
        analyze(reference, external)

if __name__ == "__main__":
    if len(sys.argv)!=2:
        print "Wrong number of arguments, can process only 1 argument. See Readme.md for examples."
    else:       
        main(sys.argv[1])

 


