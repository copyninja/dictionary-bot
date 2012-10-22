#!/usr/bin/python

import sleekxmpp
from BeautifulSoup import BeautifulSoup
from wiktionaryparser import WiktionaryParser
from xml.etree import cElementTree as ET

try:
    import simplejson as json
except:
    import json

class KNWiktionaryParser(WiktionaryParser):
    '''
      Parser for Kannada wiktionary
    '''
    def __init__(self, logger):
        WiktionaryParser.__init__(self, logger)
        self.logger = logger

    def _prepare_message(self, meanings):
        self.logger.infologger.debug(meanings)
        msg = sleekxmpp.Message()
        reply_body = ''
        reply_xml = self.xhtml_im_header
        i = 0
        for wtype in meanings.get('wtypes'):
            reply_body += '\n' + wtype + ': \n'
            reply_xml += '<br/><strong>' + wtype + ': </strong><br/>'

            defs = ','.join(meanings.get('definitions')[i])
            reply_body += defs
            reply_xml += '<p>' + defs + '</p>'

            i += 1
        reply_xml += self.xhtml_im_footer
        self.logger.infologger.info(reply_body)
        if len(reply_body) > 0:
            msg['body'] = reply_body
            msg['html']['body'] = ET.fromstring(reply_xml)
            return msg

    def get_meaning(self, data):
        meanings = {}
        wtypes = []
        meanings_list = []
        
        try:
            # Remove () from the output
            content = json.loads(data.lstrip('(').rstrip(')'))

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
            self.logger.errorlogger.exception('Something went wrong: {0}'.format(e.message))

        return self._prepare_message(meanings)
        
        



        
