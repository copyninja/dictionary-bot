from dictbot import pluginloader
import importlib


def test_pluginloader():
    "PLUGIN LOADING: Test loading plugins"
    knwiktionary = importlib.import_module("dictbot.parsers.knwiktionary")
    mlwiktionary = importlib.import_module("dictbot.parsers.mlwiktionary")
    modules = pluginloader.load_plugins()
    assert knwiktionary in modules
    assert mlwiktionary in modules
