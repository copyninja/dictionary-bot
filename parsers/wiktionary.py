from BeautifulSoup import BeautifulSoup

try:
    import simplejson as json
except ImportError:
    import json

try:
    from functools import lru_cache
except ImportError:
    from repoze.lru import lru_cache
import requests

_wiki_url = "http://%s.wiktionary.org/w/api.php?action=parse&format=json" + \
            "&prop=text|revid|displaytitle&callback=?&page=%s'"


@lru_cache(maxsize=512)
def fetch_meaning(langid, word):
    r = requests.get(_wiki_url % (langid, word))
    datajson = None
    if r.status_code == 200:
        try:
            datajson = json.loads(r.text.split('(')[1].split(')')[0])
        except Exception as e:
            raise e

        if "error" in datajson:
            raise WiktionaryPageNotFound(langid, word)

        return datajson


class WiktionaryPageNotFound(Exception):

    def __init__(self, langid, word):
        self.langid = langid
        self.word = word

    def __str__(self):
        print(">> page %s not found" % (_wiki_url % (self.langid, self.word)))


class WiktionaryParser:
    __slots__ = ["meanings", "logger", "langid", "word"]

    def __init__(self, langid, word, logger):
        self.logger = logger
        self.langid = langid
        self.word = word

    def get_meaning(self):
        self.meanings = {}
        wtypes = []
        meanings_list = []

        try:
            html_content = fetch_meaning(self.langid, self.word)
            soup = BeautifulSoup(html_content)

            # H3 has word type
            h3s = soup.findAll("h3")
            for h3 in h3s:
                wtypes.append(h3.find("span", {
                    "class": "mw-headline"
                    }).string)

            ols = soup.findAll("ol")
            for ol in ols:
                def_list = []
                for li in ol.findAll("li"):
                    for a in li.findAll("a"):
                        def_list.append(a.string)
                meanings_list.append(def_list)

            self.meanings['wtypes'] = wtypes
            self.meanings['definitions'] = meanings_list
        except Exception as e:
            self.logger.errorlogger.exception
            ('Something went wrong: {0}'.format(e.message))
