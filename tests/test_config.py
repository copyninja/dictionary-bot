from dictbot.config import loadconfig, IncompleteConfigError,\
    ParserFileMissingError


def test_validconfig():
    "CONFIGTEST: Valid Config"
    cdict = loadconfig("tests/resources/confs/valid.conf")
    assert ("debug" in cdict) is True
    assert ("jabber" in cdict) is True
    assert ("parsers" in cdict) is True


def test_invalidconfig():
    "CONFIGTEST: Invalid Config"
    try:
        loadconfig("tests/resources/confs/missing-jabber.conf")
    except IncompleteConfigError as i:
        assert i.section == "jabber"
        assert i.option is None

    try:
        loadconfig("tests/resources/confs/invalid-parser.conf")
    except ParserFileMissingError as p:
        assert p.parser == "somewiktionary"

    try:
        loadconfig("tests/resources/confs/missing-accounts.conf")
    except IncompleteConfigError as i:
        assert i.section == "jabber"
        assert i.option == "account"

    try:
        loadconfig("tests/resources/confs/missing-jid.conf")
    except IncompleteConfigError as i:
        assert i.section == "account"
        assert i.option == "jid"

    try:
        loadconfig("tests/resources/confs/missing-password.conf")
    except IncompleteConfigError as i:
        assert i.section == "account"
        assert i.option == "password"

    try:
        loadconfig("tests/resources/confs/missing-lang.conf")
    except IncompleteConfigError as i:
        assert i.section == "account"
        assert i.option == "lang"
