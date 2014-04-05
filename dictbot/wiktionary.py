from bs4 import BeautifulSoup
from guesslanguage import getInstance
from abc import ABCMeta, abstractmethod, abstractproperty

try:
    from functools import lru_cache
except ImportError:
    from repoze.lru import lru_cache

import requests
import json

_wiki_url = "http://%s.wiktionary.org/w/api.php?action=parse&format=json" + \
            "&prop=text|revid|displaytitle&callback=?&page=%s'"


class WiktionaryPageNotFoundError(Exception):

    def __init__(self, langid, word):
        self.langid = langid
        self.word = word

    def __str__(self):
        return ">> page %s not found" % (_wiki_url % (self.langid, self.word))


class WiktionaryParser(object):
    """
    Base Class for Wiktionary parsers implements some abstract
    method which can be overriden by new parsers
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        self._langid = None

    @abstractproperty
    def langid(self):
        return self._langid

    @langid.setter
    def langid(self, lang):
        self._langid = lang
        self._langguesser = getInstance()

    @staticmethod
    @lru_cache(maxsize=512)
    def fetch_meaning(langid, word):
        r = requests.get(_wiki_url % (langid, word))
        datajson = {}
        if r.status_code == 200:
            try:
                datajson = json.loads(r.text.split('(')[1].split(')')[0])
            except Exception as e:
                raise e

            if "error" in datajson:
                raise WiktionaryPageNotFoundError(langid, word)

        return datajson["parse"]["text"]["*"]

    @abstractmethod
    def get_meaning(self, word):
        """
         Function to parse wiktionary page, this function supports
        `Kannada', `Malayalam' language wiktionary. If the language
        you want to support is not supported by this function then you
        need to override this function in your derived class.
        """
        meanings = {}
        wtypes = []
        meanings_list = []

        html_content = self.fetch_meaning(self._langid, word)
        soup = BeautifulSoup(html_content)

        # H3 has word type
        h3s = soup.findAll("h3")
        for h3 in h3s:
            wtypes.append(h3.find("span", {
                "class": "mw-headline"
            }).string)

        ols = soup.findAll("ol")
        for ol in ols:
            for li in ol.findAll("li"):
                meanings_list.append([a.string for a in li.findAll("a")])

        meanings['wtypes'] = wtypes
        meanings['definitions'] = meanings_list
        return meanings

    @abstractmethod
    def get_supported_lang(self):
        "Returns the language supported by the current parser"
