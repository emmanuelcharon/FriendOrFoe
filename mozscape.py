#! /usr/bin/env python

from lsapi import lsapi
import keys
import json

def get_backlinks(url, mozscapeAPIaccessID, mozscapeAPIkey):
   """ Uses the Mozscape API to retrieve some backlinks on a url.
       Returns a list of urls.
      """
   # mozscape needs http:// out
   if len(url)>=7 and "http://"==url[0:7]:
      url = url[7:]
   elif len(url)>=8 and "https://"==url[0:8]:
      url = url[8:]
   else:
      return None
   
   l = lsapi(mozscapeAPIaccessID, mozscapeAPIkey)
   links = l.links(url, filters=['external', 'nofollow']) 
   result = list();
   for link in links:
       result.append("http://"+link['uu'])
   return result

### Example of use
def main():
    url = "http://blog.guykawasaki.com/2005/12/the_102030_rule.html"
    mozscapeAPIaccessID = keys.mozscapeAPIaccessID               
    mozscapeAPIkey = keys.mozscapeAPIkey
    mozscape_response = get_backlinks(url, mozscapeAPIaccessID, mozscapeAPIkey)
    print json.dumps(mozscape_response, sort_keys=True, indent=4, separators=(',', ': '))

if __name__ == "__main__":
    main()
