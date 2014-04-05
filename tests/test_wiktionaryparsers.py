# -*- coding: utf-8 -*-
import sys

if sys.version_info.major == 3 and sys.version_info.minor == 3:
    from unittest import mock
else:
    import mock

import json
from mock import patch
from dictbot.parsers.knwiktionary import KNWiktionaryParser
from dictbot.parsers.mlwiktionary import MLWiktionaryParser


def data_from_resource(filename):
    with open(filename) as fd:
        content = fd.read()
        return json.loads(content.split('(', 1)[1].rsplit(')', 1)[0])


@patch.object(KNWiktionaryParser, 'fetch_meaning')
def test_knwiktionaryparser(mock_method):
    mock_method.return_value = data_from_resource(
        "tests/resources/parsers/kn.dat")["parse"]["text"]["*"]
    instance = KNWiktionaryParser()
    actoutput = instance.get_meaning("mango")
    expectoutput = {
        "wtypes": [u"ನಾಮಪದ"],
        "definitions": [[u"ಮಾವು", u"ಆಮ್ರ", u"ಮಾವಿನ ಮರ"],
                        [u"ಮಾವಿನ ಕಾಯಿ", u"ಮಾವಿನ ಹಣ್ಣು"]]
    }
    assert actoutput == expectoutput


@patch.object(MLWiktionaryParser, 'fetch_meaning')
def test_mlwiktionaryparser(mock_method):
    mock_method.return_value = data_from_resource(
        "tests/resources/parsers/ml.dat")["parse"]["text"]["*"]
    instance = MLWiktionaryParser()
    actoutput = instance.get_meaning("mango")
    expectoutput = {
        "wtypes": [],
        "definitions": [[u"മാമ്പഴം"], [u"മാവ്‌"], [u"ആമ്രം"],
                        [u"ചൂതം"], [u"ആമ്രഫലം"], [u"ചൂതഫലം"],
                        [u"മാവ്‌"], [u"ആമ്രം"], [u"പികവല്ലഭം"],
                        [u"പികരാഗം"], [u"മാവിൻതോട്ടം"], [u"മാങ്ങയണ്ടി"],
                        [u"കണ്ണിമാങ്ങ"], [u"ഉണ്ണി", u"മാങ്ങ"],
                        [u"മൽഗോവാമാമ്പഴം"],
                        [u"മാമ്പൂവ്‌"], [u"ഉപ്പിലിട്ട", u"മാങ്ങ"]]
    }
    assert actoutput == expectoutput
