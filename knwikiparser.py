#!/usr/bin/python


from urllib2 import Request, urlopen
from BeautifulSoup import BeautifulSoup

try:
    import simplejson as json
except:
    import json

class KNWiktionaryParser:
    '''
      Parser for Kannada wiktionary
    '''
    def __init__(self, url, logger):
        self.url = url
        self.logger = logger

    def __connect(self, word):
        request = Request(self.url + word)
        request.add_header('User-Agent',"Mozilla/5.0")
        response = None
        
        try:
            response = urlopen(request).read()
        except Exception as e:
            self.logger.exception('Error occured for URL: {0} reason: {1}'.format(self.url,e.message))

        return response

    def get_meaning(self, word):
        self.logger.debug(word)
        meanings = {}
        wtypes = []
        meanings_list = []
        
        try:
            # Remove () from the output
            tmp = self.__connect(word).lstrip('(').rstrip(')')
            content = json.loads(tmp)

            html_content = content.get('parse').get('text').get('*')
            soup = BeautifulSoup(html_content)

            # H3 has word type
            h3s = soup.findAll("h3")
            for h3 in h3s:        
                wtypes.append(h3.find("span",{
                    "class" : "mw-headline"
                    }).string)
                    
            ols = soup.findAll("ol")
            for ol in ols:
                def_list = []
                for li in ol.findAll("li"):
                    for a in li.findAll("a"):
                        def_list.append(a.string)
                meanings_list.append(def_list)
                
            meanings['wtypes'] = wtypes
            meanings['definitions'] = meanings_list
        except Exception as e:
            self.logger.exception('Something went wrong: {0}'.format(e.message))
            pass

        return meanings
        
        



        
