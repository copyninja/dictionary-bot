#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# eng-kn-bot.py A Jabber buddy bot which provide eng-mal dictionary lookup service
#       
# Copyright (c) 2009
#     Santhosh Thottingal <santhosh.thottingal@gmail.com>
#     Sarath Lakshman <sarathlakshman@gmail.com> 
#     Ragsagar <ragsagar@gmail.com>
# Swathanthra Malayalam Computing(http://smc.org.in/)
# Copyright (c) 2010
#     Vasudev Kamath
# Sanchaya Group (http://sanchaya.net)
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#       
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import xmpp
from xmpp.protocol import *
from loghandler import get_logger
from daemonize import *
import wiktionary
import sqlite3
import re
import hunspell


# English word suggestions
hun = hunspell.HunSpell('/usr/share/myspell/dicts/en_US.dic', '/usr/share/myspell/dicts/en_US.aff')



# Jabber auth
options = {
#    'JID': 'kn.dict.bot@jabber.org',
    'JID': 'kn-dictionary-bot@jabber.org',
    'Password': 'k4d4abotdictionary',
}
 
class ConnectionError: pass
class AuthorizationError: pass
class NotImplemented: pass


INSERT_MEANING = "INSERT INTO users_meanings (word,meaning,user) values ('%s','%s','%s')"

welcome_output = """ನಮಸ್ಕಾರ!
ನಾನು ಇಂಗ್ಲೀಷ್ - ಕನ್ನಡ ಡಿಕ್ಷನರಿ ಬಾಟ್
ನಾನು ಕನ್ನಡ ವೀಕ್ಷ್ನರಿಯ ಸಹಾಯದಿಂದ ಪದಗಳ ಅರ್ಥವನ್ನು ಹೇಳಬಲ್ಲೆ.
ಅರ್ಥ ತಿಳಿಯಲು ಶಬ್ದವನ್ನು ನನಗೆ ಕಳುಹಿಸಿ.
ಶುಭ ದಿನ!"""

not_found_output = """
ನೀವು ಪದಕ್ಕೆ ಅರ್ಥ ಸೇರಿಸಬೇಕಿದ್ದರೆ,
#add english-word: ಕನ್ನಡದ ಅರ್ಥ
ಬರೆದು ಕಳಿಸಿ.ಒಂದಕ್ಕಿಂತ ಹೆಚ್ಚು ಅರ್ಥಗಳಿದ್ದರೆ "," ಬಳಸಿ.  
"""

thanks_output = """
ಪದವನ್ನು ಸೇರಿಸಿದ್ದಕ್ಕೆ ಧನ್ಯವಾದಗಳು.
ಎಲ್ಲಾ ಪದಗಳನ್ನು ವಿಕಿಷನರಿ ತಂಡಕ್ಕೆ ಕಳಿಸಬೇಕಾದ್ದರಿಂದ ಸಲ್ಪ ಸಮಯ ತೆಗೆದುಕೊಳ್ಳುತ್ತದೆ.
ಒಮ್ಮೆ ಪದಗಳನ್ನು ವಿಕಿಷನರಿ ಗೆ ಸೇರಿಸಿದ ಬಳಿಕ ಅವನ್ನು ಬಳಸಬಹುದು. 
"""

meanings_pattern = re.compile('#add\s([a-zA-z\s]+):\s(.+)')

class Bot:
    """ The main bot class. """

    def __init__(self,logger, JID, Password):
        """ Create a new bot. Connect to the server and log in. """

        self.logger = logger
        # connect...
        jid = xmpp.JID(JID)
        self.connection = xmpp.Client(jid.getDomain(), debug=[])
        self.en_ml_db = None
        result = self.connection.connect()

        if result is None:
            raise ConnectionError

        # authorize
        result = self.connection.auth(jid.getNode(), Password)

        if result is None:
            raise AuthorizationError

        self.connection.RegisterHandler('presence',self.presenceHandler)
        self.connection.RegisterHandler('message',self.messageHandler)
        # ...become available
        self.connection.sendInitPresence()


    def loop(self):
        """ Do nothing except handling new xmpp stanzas. """
        try:
            while self.connection.Process(1):
                pass
        except KeyboardInterrupt:
            pass
            
    def messageHandler(self, conn,message_node):
        word = message_node.getBody()
        output= ""
        if  word :
            if word.lower() == "hi" or word.lower() == "hello":
                output = welcome_output
            elif word.startswith("#add"):
                message = meanings_pattern.findall(word)
                if len(message) < 1 or len(message[0]) < 2:
                    output = not_found_output
                else:
                    self.add_meaning(message[0][0],message[0][1],message_node.getFrom())
                    output = thanks_output
            else:    
                wikioutput  = wiktionary.get_def(word.lower(), "kn_IN","kn_IN")
                if wikioutput:
                    output += wikioutput.encode("utf-8")
                if wikioutput==None:
                    output = "ಕ್ಷಮಿಸಿ ಈ ಶಬ್ದದ ಅರ್ಥವು ನನಗೆ ತಿಳಿದಿಲ್ಲ!\n" + not_found_output
                suggestion_output = ""

                try:
                    if not hun.spell(word.lower()):
                        suggestions = hun.suggest(word.lower())

                        for suggestion in suggestions:
                            if not (wiktionary.get_def(suggestion)):
                                suggestion_output += "\t" + suggestion + "\n"
                except:
                    pass
                if suggestion_output > "":
                    output += u"ಸಲಹೆಗಳು: \n" + suggestion_output
                                
            conn.send( xmpp.Message( message_node.getFrom() ,output))    
                    
    def presenceHandler(self, conn, presence):
        '''Auto authorizing chat invites''' 
        if presence:
            if presence.getType() == 'subscribe':
                jabber_id = presence.getFrom().getStripped()
                self.connection.getRoster().Authorize(jabber_id)
            #self.logger.debug(presence.getFrom().getStripped())

    def add_meaning(self,word,meaning,user):
        global INSERT_MEANING
        conn = sqlite3.connect('/home/vasudev/kannada-dictionary-bot/wiktionary.sqlite')
        c = conn.cursor()
        c.execute(INSERT_MEANING % (word,meaning,user))
        conn.commit()
        c.close()
        conn.close()

if __name__ == "__main__":
    # Configure the Daemon
    set_lockfile("eng-kn-bot.pid")
    set_logfile("eng-kn-bot.log")
    
    daemonizer()

    # Get logger this is done later to avoid closing logger files when daemonizing
    logger = get_logger('kn-dictionary-bot',get_daemon_log(),"debug") # only error and exceptions are logged
    try:
        bot = Bot(logger,**options)
        bot.loop()
    except:
        logger.exception("Something Went Wrong!")

