import urllib2
import json
import keys

def extract_article(url, diffbotAPIkey):
    """Uses the Diffbot article API to fetch relevant data from the url.
       Data is retruned as a json object."""
    
    request = "http://www.diffbot.com/api/article?token="+diffbotAPIkey+"&url="+url
    response = urllib2.urlopen(request).read()
    response = json.loads(response)
    return response

def is_article(url, diffbotAPIkey):
    """Uses the Diffbot analyze API to determine if a link is an article or blog post or not.
       Returns a boolean. """

    request = "http://www.diffbot.com/api/analyze?token="+diffbotAPIkey+"&url="+url
    response = urllib2.urlopen(request).read()
    response = json.loads(response)
    if response["type"] and response["type"]=="article":
        return True
    else:
        return False

### Example of use
def main():
    url = "http://www.nytimes.com/2013/06/02/health/colonoscopies-explain-why-us-leads-the-world-in-health-expenditures.html"    
    diffbotAPIkey = keys.diffbotAPIkey
    diffbot_response = extract_article(url, diffbotAPIkey)
    print json.dumps(diffbot_response, sort_keys=True, indent=4, separators=(',', ': '))

if __name__ == "__main__":
    main()

    
