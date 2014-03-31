from dictbot.parsers.wiktionary import WiktionaryParser


class KNWiktionaryParser(WiktionaryParser):

    def __init__(self):
        super(KNWiktionaryParser, self).__init__()

    @property
    def langid(self):
        return super(KNWiktionaryParser, self).langid

    @langid.setter
    def langid(self, value):
        super(KNWiktionaryParser, self).langid = value

    def get_meaning(self, word):
        return super(KNWiktionaryParser, self).get_meaning(word)


def get_instance():
    return KNWiktionaryParser()
