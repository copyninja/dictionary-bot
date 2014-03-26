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
            print(">> Missing option %s in section %s" %
                  (self.option, self.section))
        else:
            print(">> Missing section %s" % (self.section))


def loadconfig(location="/etc/dictbot.conf"):
    with open(location, "r") as fd:
        configdict = load(fd, Loader=Loader)
        _verify(configdict)
        return configdict


def _verify(configdict):
    if not "jabber" in configdict:
        raise IncompleteConfigError("jabber", None)

    if len(configdict.get('jabber')) == 0:
        raise IncompleteConfigError("jabber", "account")
    else:
        for acnt in configdict.get('jabber'):
            if not "lang" in acnt:
                raise IncompleteConfigError("account", "lang")

    if not "debug" in configdict:
        configdict['debug'] = False
