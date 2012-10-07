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
        def_list = []
        wtype = ""            
        try:
            # Remove () from the output
            tmp = self.__connect(word).lstrip('(').rstrip(')')
            content = json.loads(tmp)

            html_content = content.get('parse').get('text').get('*')
            soup = BeautifulSoup(html_content)

            # H3 has word type
            h3 = soup.find("h3")
            wtype = h3.find("span",{
                    "class" : "mw-headline"
                    }).string
            meaning_list = soup.find("ol")
            for li in meaning_list.findAll("li"):
                for a in li.findAll("a"):
                    def_list.append(a.string)
        except Exception as e:
            self.logger.exception('Something went wrong: {0}'.format(e.message))
            self.logger.debug('Message fetched from wiktionary:\n' + soup.string)
            pass
        
        return (wtype,','.join(def_list)) if len(word) > 0 and len(wtype) > 0 and len(def_list) > 0 else None
        
    def __bs_preprocess(self,html):
        html = html.replace("&lt;","<")
        html = html.replace("&gt;",">")
        html = html.replace('&quot;','\'')
        return html 

        



        
