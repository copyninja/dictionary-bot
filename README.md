Dictionary Bot
==============

[![Build Status](https://travis-ci.org/copyninja/dictionary-bot)](https://travis-ci.org/copyninja/dictionary-bot)

This is a extensible an XMPP based bot for fetching meanings for given
word from various sources. Currently implemented source is Wiktionary
other source can be added in future.

Parser for each source should be added as plugin under parsers
directory which will be loaded during run time.

TODO
----
*~Enable multiple account login~
* Enable meaning collection using XEP-0004 (DataForms)
*~Move the xml construction logic totally to bridge to avoid polluting
   wiktionary parsers~
*~Write test cases~
*~Enable CI for continuous integration~
