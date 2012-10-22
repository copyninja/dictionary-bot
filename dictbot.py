#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
import os
import sleekxmpp
import yaml
import logging

from argparse import ArgumentParser
from bridge import ParserBridge
from loghandler import LogHandler

# Python versions before 3.0 do not use UTF-8 encoding
# by default. To ensure that Unicode is handled properly
# throughout SleekXMPP, we will set the default encoding
# ourselves to UTF-8.
if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input


class DictBot(sleekxmpp.ClientXMPP):
    """
      A dictionary bot which recieves words as input from any language
      looks up the meaning from the respective wiktionary and responds
      with proper formatted output

      If meaning is not found it responds with a data form asking user
      to input the meanings types etc.
    """
    def __init__(self, jid, password, logger, lang='kn_IN'):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        
        self.register_plugin('xep_0030')  # Service Discovery
        self.register_plugin('xep_0004')  # Data Forms
        self.register_plugin('xep_0060')  # PubSub
        self.register_plugin('xep_0199')  # XMPP Ping

        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)

        self.auto_authorize = True
        self.logger = logger
        self.lang = lang

    def start(self, event):
        """
         Process the session_start event.

         Typical actions for the session_start event are
         requesting the roster and broadcasting an initial
         presence stanza.

         :param event: An empty dictionary. The session_start
                       event does not provide any additional
                       data
        """
        self.send_presence()
        self.get_roster()

    def message(self, msg):
        """
         Process the message stanza from client basically this
         will be request from the user containing single word
         but some time might be error message so before proceeding
         with processing of the message it is better to check type
         of message.

         If message is valid chat type pass it on to the bridge
         code to do further processing and wait for result.

         :param msg: Message object representing the message from
                     client.
        """

        if msg['type'] in ('chat', 'normal'):
            #TODO: pass this to the bridge for further processing
            reply = ParserBridge(msg, self.lang, self.logger).process()
            if reply:
                reply.send()
            else:
                pass


def main():
    """
     Main driver for the bot. First check for the configuration file
     and load values from it. Then check if the same value is passed
     as arguments then override the value from the configuration file

     Once values are obtained then start the bot
    """

    custompathstem = os.path.join(os.environ['DICTBOT_CONFIGDIR'],
                                  'dictbot.conf') \
                                  if 'DICTBOT_CONFIGDIR' in os.environ \
                                  else None
    
    log_file = os.path.join(os.environ['DICTBOT_LOGDIR'],
                                 'dictbot.log')\
                                 if 'DICTBOT_LOGDIR' in os.environ \
                                 else '/var/log/dictbot.log'

    config_file = custompathstem if custompathstem and os.path.exists(
        custompathstem)\
        else '/etc/dictbot/dictbot.conf'

    
    configdict = yaml.load(file(config_file).read())

    parser = ArgumentParser(description='A Jabber Dictionary Bot')
    parser.add_argument(
                        '-j', '--jid',
                        help='Jabber ID for the bot to connect.',
                        required=False)
    parser.add_argument(
                        '-p', '--password',
                        help='Password for Jabber account',
                        required=False)

    parser.add_argument('-d', '--debug', help='set logging to DEBUG',
                    action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.INFO)

    args = parser.parse_args()

    jid = configdict.get('jabber').get('jid')\
        if 'jabber' in configdict and\
        'jid' in configdict.get('jabber') else args.jid
    password = configdict.get('jabber').get('password')\
        if 'jabber' in configdict\
        and 'password' in configdict.get('jabber') else args.password

    if not jid or not password:
        print """Please provide JID and Password either through config or
 command line options"""
        sys.exit(2)

    debug = logging.DEBUG if 'debug' in configdict and\
        configdict.get('debug') == 1 else args.debug
    logger = LogHandler(debug, log_file)
    logging.basicConfig(level=debug,
                       format='%(levelname)-8s %(message)s')    

    xmpp = DictBot(jid, password, logger)

    if xmpp.connect():
        xmpp.process(block=True)
    else:
        print "Unable to connect"

if __name__ == "__main__":
    main()
