#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import yaml
import xml.etree.ElementTree as ET

from logging.handlers import TimedRotatingFileHandler

from constants import *
from knwikiparser import KNWiktionaryParser

from pyxmpp2.jid import JID
from pyxmpp2.message import Message
from pyxmpp2.presence import Presence
from pyxmpp2.client import Client
from pyxmpp2.settings import XMPPSettings
from pyxmpp2.interfaces import EventHandler, event_handler, QUIT
from pyxmpp2.streamevents import AuthorizedEvent, DisconnectedEvent
from pyxmpp2.interfaces import XMPPFeatureHandler
from pyxmpp2.interfaces import presence_stanza_handler, message_stanza_handler
from pyxmpp2.ext.version import VersionProvider


class DictBot(EventHandler, XMPPFeatureHandler):
    '''
     Dictionary bot implementation
    '''
    def __init__ (self, my_jid, settings, logger, url, lang):
        version_provider = VersionProvider(settings)
        self.client = Client(my_jid, [self, version_provider], settings)
        self.logger = logger
        self.parser = None
        if lang == 'kn':
            self.parser = KNWiktionaryParser(url, self.logger)
        
    def run(self):
        '''
         Request client connection and start mainloop
        '''
        self.client.connect()
        self.client.run()

    def disconnect(self):
        '''
         Request disconnection and let the main loop run for a 2 more
         seconds for graceful disconnection
        '''
        self.client.disconnect()
        self.client.run(timeout=2)
    @presence_stanza_handler("subscribe")
    def handle_presence_subscribe(self, stanza):
        self.logger.info(u"{0} requested presence subscription"
                                                    .format(stanza.from_jid))
        presence = Presence(to_jid = stanza.from_jid.bare(),
                                                    stanza_type = "subscribe")
        return [stanza.make_accept_response(), presence]

    @presence_stanza_handler("subscribed")
    def handle_presence_subscribed(self, stanza):
        self.logger.info(u"{0!r} accepted our subscription request"
                                                    .format(stanza.from_jid))
        return True

    @presence_stanza_handler("unsubscribe")
    def handle_presence_unsubscribe(self, stanza):
        self.logger.info(u"{0} canceled presence subscription"
                                                    .format(stanza.from_jid))
        presence = Presence(to_jid = stanza.from_jid.bare(),
                                                    stanza_type = "unsubscribe")
        return [stanza.make_accept_response(), presence]

    @presence_stanza_handler("unsubscribed")
    def handle_presence_unsubscribed(self, stanza):
        self.logger.info(u"{0!r} acknowledged our subscrption cancelation"
                                                    .format(stanza.from_jid))
        return True

    @message_stanza_handler()
    def handle_message(self, stanza):
        """
          Handle the request messages
        """
        if stanza.subject:
            subject = u"Re: " + stanza.subject
        else:
            subject = None

        if stanza.body:
            msg = Message(stanza_type = stanza.stanza_type,
                          from_jid = stanza.to_jid, to_jid = stanza.from_jid,
                          subject = subject,thread = stanza.thread)  
            body = stanza.body.lower().strip()
            if body == 'hello' or body == 'hi':
                msg.body = welcome_output.decode('utf-8')
            elif not body.startswith('#'):
                meanings = self.parser.get_meaning(body)
                reply = self._prepare_reply(meanings)
                if reply:
                    msg.body,xml_payload = reply
                    tree = ET.fromstring(xml_payload)
                    msg.add_payload(tree)                                
                else:
                    msg.body = u"ಕ್ಷಮಿಸಿ ಈ ಶಬ್ದದ ಅರ್ಥವು ನನಗೆ ತಿಳಿದಿಲ್ಲ!\n"
                    
            return msg

    def _prepare_reply(self, meanings):
        reply = ''
        xml = xhtml_im_header
        i = 0
        for wtype in meanings.get('wtypes'):
            reply += '\n' + wtype + ': \n'
            xml += '<br/><strong>' + wtype +': </strong><br/>'
            
            defs = meanings.get('definitions')
            
            reply += ','.join(defs[i])
            xml += '<p>' + ','.join(defs[i]) + '</p><br/>'
            i += 1

        xml += xhtml_im_footer
        self.logger.debug(reply)
        
        return (reply,xml.encode('utf-8')) if len(reply) > 0 else None

    @event_handler(DisconnectedEvent)
    def handle_disconnected(self, event):
        """Quit the main loop upon disconnection."""
        return QUIT
    
    @event_handler()
    def handle_all(self, event):
        """Log all events."""
        self.logger.info(u"-- {0}".format(event))

        
def prepare_logger(debug=0):
    handler = TimedRotatingFileHandler('dictbot.log', when='D', interval=7)
    logger = logging.getLogger('dictbot')
    
    if debug == 1:
        handler.setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)
    else:
        handler.setLevel(logging.ERROR)
        logger.setLevel(logging.ERROR)
        
    logger.addHandler(handler)

    return logger

    
def main():
    conffile = 'dictbot.conf' if os.path.exists(os.path.join(os.path.dirname(__file__),
                                                             "dictbot.conf")) else "/etc/dictbot.conf"
    config = yaml.load(open(conffile).read())
    network_section = config.get('network')
    wiktionary_section = config.get('wiktionary')
    authorization_section = config.get('authorization')
    
    jid = authorization_section.get('jabber_id')
    password = authorization_section.get('password')
    
    server = network_section.get('server')
    prefer_ipv6 = network_section.get('prefer_ipv6')
    starttls = True if network_section.get('starttls') == 1 else False

    language = wiktionary_section.get('language')
    api_url = wiktionary_section.get('wiktionary_url')
    url = 'http://' + language + '.' + api_url
    
    debug = True if config.get('debug') == 1 else False


    if debug:
        logger = prepare_logger(1)
    else:
        logger = prepare_logger(0)
        
    settings = XMPPSettings({
            'password': password,
            'prefer_ipv6':prefer_ipv6,
            'server': server,
            'starttls': starttls
            })
    
    bot = DictBot(JID(jid), settings, logger, url, language)
    try:
        bot.run()
    except KeyboardInterrupt:
        bot.disconnect()

if __name__ == '__main__':
    main()
