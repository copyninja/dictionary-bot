#!/usr/bin/python

from wiktionaryparsers.knwikiparser import KNWiktionaryParser
from guesslanguage import getInstance
from httphandler import connect

from sleekxmpp import Message

__wiktionary_url__ = 'wiktionary.org/w/api.php?action=parse&format=json&prop=text|revid|displaytitle&callback=?&page='

class ParserBridge:
    """
      A Bridge between bot and the parsing logic
    """
    def __init__(self, msg, lang, logger):
        """
          Initialize the bridge object
          
         :param msg: Message stanza from the bot which
                     needs to be processed
        """
        self.body = msg['body'].strip()
        self.from_id = msg['from']
        self.to_id = msg['to']
        self.subject = msg['subject']
        self.id = msg['id']
        self.type = msg['type']
        self.langguesser = getInstance()
        self.logger = logger
        self.lang = lang
        
        self.parserdict = {
             'kn_IN':KNWiktionaryParser(self.logger),
            }
        

    def _process_word(self, langid, word):
        parser = self.parserdict.get(langid)
        url = 'http://' + langid.split('_')[0] + '.' + __wiktionary_url__ + word
        data = connect(url)
        if data and type(data).__name__ == 'str':
            return parser.get_meaning(data)
        else:
            self.logger.errorlogger.exception('Something went wrong: {0} and {1}'.format(data.message, url))
            
    def process(self):
        message = None
        if len(self.body.split()) > 1:
            print 'inside muliword'
            # We have more than one please send back an error
            return "Sorry please send me one word at a time!"
        else:
            langid = self.langguesser.guessLanguageId(self.body)
            if langid in self.parserdict:
                message = self._process_word(langid, self.body)
            elif langid == 'en_US':
                message = self._process_word(self.lang, self.body)
        return message 
