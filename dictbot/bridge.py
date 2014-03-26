#!/usr/bin/python

from parser import wiktionary
from guesslanguage import getInstance


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

    def process(self):
        message = None
        if len(self.body.split()) > 1:
            # We have more than one please send back an error
            return "Sorry please send me one word at a time!"
        else:
            langid = self.langguesser.guessLanguageId(self.body)
            if langid in self.parserdict:
                message = self._process_word(langid, self.body)
            elif langid == 'en_US':
                message = self._process_word(self.lang, self.body)
        return message
