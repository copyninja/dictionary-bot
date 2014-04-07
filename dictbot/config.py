from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


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


def loadconfig(location="/etc/dictbot.conf"):
    with open(location, "r") as fd:
        configdict = load(fd, Loader=Loader)
        _verify(configdict)
        return configdict


def _verify(configdict):
    if "jabber" not in configdict:
        raise IncompleteConfigError("jabber", None)

    if configdict.get('jabber') is None or \
       len(configdict.get('jabber')) == 0:
        raise IncompleteConfigError("jabber", "account")
    else:
        for acnt in configdict.get('jabber'):
            if "lang" not in acnt:
                raise IncompleteConfigError("account", "lang")
            elif "jid" not in acnt:
                raise IncompleteConfigError("account", "jid")
            elif "password" not in acnt:
                raise IncompleteConfigError("account", "password")
            elif "plugins" not in acnt or len(acnt["plugins"]) == 0:
                raise IncompleteConfigError("account", "plugins")

    if "debug" not in configdict:
        configdict['debug'] = False
    else:
        configdict['debug'] = True if configdict['debug'] == 1 else False
