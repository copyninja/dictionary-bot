from dictbot.parsers.wiktionary import WiktionaryParser


class MLWiktionaryParser(WiktionaryParser):

    def __init__(self):
        super(MLWiktionaryParser, self).__init__()

    @property
    def langid(self):
        return super(MLWiktionaryParser, self).langid

    @langid.setter
    def langid(self, value):
        super(MLWiktionaryParser, self).langid = value

    def get_meaning(self, word):
        return super(MLWiktionaryParser, self).get_meaning(word)


def get_instance():
    return MLWiktionaryParser()
