from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

import os


class IncompleteConfigError(Exception):
    def __init__(self, section, option):
        self.section = section
        self.option = option

    def __str__(self):
        if self.option is not None:
            return ">> Missing option %s in section %s" % \
                (self.option, self.section)
        else:
            return ">> Missing section %s" % (self.section)


class ParserFileMissingError(Exception):
    def __init__(self, parser):
        self.parser = parser

    def __str__(self):
        return ">> Parser file %s.py doesn't exist" % \
            (self.parser)


def loadconfig(location="/etc/dictbot.conf"):
    with open(location, "r") as fd:
        configdict = load(fd, Loader=Loader)
        _verify(configdict)
        return configdict


def _verify(configdict):
    if not "jabber" in configdict:
        raise IncompleteConfigError("jabber", None)

    if configdict.get('jabber') is None or \
       len(configdict.get('jabber')) == 0:
        raise IncompleteConfigError("jabber", "account")
    else:
        for acnt in configdict.get('jabber'):
            if not "lang" in acnt:
                raise IncompleteConfigError("account", "lang")
            elif not "jid" in acnt:
                raise IncompleteConfigError("account", "jid")
            elif not "password" in acnt:
                raise IncompleteConfigError("account", "password")

    if len(configdict.get('parsers')) == 0:
        raise IncompleteConfigError("parsers", None)
    else:
        for fp in configdict.get('parsers'):
            if not os.path.exists(os.path.join("dictbot", "parsers", fp) +
                                  ".py"):
                raise ParserFileMissingError(fp)

    if not "debug" in configdict:
        configdict['debug'] = False
    else:
        configdict['debug'] = True if configdict['debug'] == 1 else False
