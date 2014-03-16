#!/usr/bin/python

from BeautifulSoup import BeautifulSoup
from wiktionaryparser import WiktionaryParser

try:
    import simplejson as json
except:
    import json


class MLWiktionaryParser(WiktionaryParser):
    '''
      Parser for Malayalam wiktionary
    '''

    def __init__(self, logger):
        WiktionaryParser.__init__(self, logger)
        self.logger = logger

    def get_meaning(self, data):
        self.meanings = {}
        wtypes = []
        meanings_list = []

        try:
            tmp = data.lstrip('(').rstrip(')')
            content = json.loads(tmp)

            html_content = content.get('parse').get('text').get('*')
            soup = BeautifulSoup(html_content)

            h3s = soup.findAll("h3")
            for h3 in h3s:
                wtypes.append(h3.find("span", {
                    "class": "mw-headline"}).string)

            ols = soup.findAll("ol")
            for ol in ols:
                def_list = []
                for li in ol.findAll("li"):
                    for a in li.findAll("a"):
                        def_list.append(a.string)
                meanings_list.append(def_list)

            self.meanings['wtypes'] = wtypes
            self.meanings['definitions'] = meanings_list
        except Exception as e:
            self.logger.errorlogger.exception
            ('Something went wrong: {0}'.format(e.Message))
