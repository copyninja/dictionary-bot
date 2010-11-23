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

# Configure the Daemon
set_lockfile("eng-kn-bot.pid")
set_logfile("eng-kn-bot.log")
logger = get_logger('kn-dictionary-bot',get_daemon_log(),"error") # only error and exceptions are logged


# Jabber auth
options = {
    'JID': 'kn-dictionary-bot@jabber.org',
    'Password': 'k4d4abotdictionary',
}
 
class ConnectionError: pass
class AuthorizationError: pass
class NotImplemented: pass


welcome_output = """ನಮಸ್ಕಾರ!
ನಾನು ಇಂಗ್ಲೀಷ್ - ಕನ್ನಡ ಡಿಕ್ಷನರಿ ಬಾಟ್
ನಾನು ಕನ್ನಡ ವೀಕ್ಷ್ನರಿಯ ಸಹಾಯದಿಂದ ಪದಗಳ ಅರ್ಥವನ್ನು ಹೇಳಬಲ್ಲೆ.
ಅರ್ಥ ತಿಳಿಯಲು ಶಬ್ದವನ್ನು ನನಗೆ ಕಳುಹಿಸಿ.
ಶುಭ ದಿನ!"""


class Bot:
    """ The main bot class. """

    def __init__(self, JID, Password):
        """ Create a new bot. Connect to the server and log in. """

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
            else:    
                wikioutput  = wiktionary.get_def(word, "kn_IN","kn_IN")
                if wikioutput:
                    output += wikioutput.encode("utf-8")
                if wikioutput==None:
                    output = "ಕ್ಷಮಿಸಿ ಈ ಶಬ್ದದ ಅರ್ಥವು ನನಗೆ ತಿಳಿದಿಲ್ಲ!"
            conn.send( xmpp.Message( message_node.getFrom() ,output))    
                    
    def presenceHandler(self, conn, presence):
        '''Auto authorizing chat invites''' 
        if presence:
            if presence.getType() == 'subscribe':
                jabber_id = presence.getFrom().getStripped()
                self.connection.getRoster().Authorize(jabber_id)
            logger.debug(presence.getFrom().getStripped())
            

if __name__ == "__main__":
    try:
        daemonizer()
        bot = Bot(**options)
        bot.loop()
    except:
        logger.exception("Something Went Wrong!")

