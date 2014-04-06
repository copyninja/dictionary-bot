#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from logging.handlers import RotatingFileHandler
from dictbot.accounthandler import JabberAccount
from dictbot.config import loadconfig
from multiprocessing import Process


ROOT = "/etc"


def spawn_newbot(jid, password, lang, plugins):
    xmpp = JabberAccount(jid, password, lang, plugins)
    if xmpp.connect():
        xmpp.process(block=True)
    else:
        logger = logging.getLogger('dictbot')
        logger.error("Unable to connect for {jid}".format(jid=jid))


def main():
    configdict = loadconfig("{root}/dictbot.conf".format(root=ROOT))
    logger = logging.getLogger("dictbot")
    logger.setLevel(logging.DEBUG if configdict.get('debug') else logging.INFO)
    handler = RotatingFileHandler("/var/log/dictbot.log", maxBytes=10000000,
                                  backupCount=10)
    formatter = logging.Formatter('[dictbot] %(levelname)7s - %(message)s')
    logger.setFormatter(formatter)
    logger.addHandler(handler)
    logging.info("Booting up  Dictbot")

    for acnt in configdict.get('jabber'):
        p = Process(target=spawn_newbot,
                    args=(acnt.get('jid'),
                          acnt.get('password'),
                          acnt.get('lang'),
                          acnt.get('plugins')))
        p.start()
        p.join(15)
