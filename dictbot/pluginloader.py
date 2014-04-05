import importlib
import os
import re


def load_plugins():
    filere = re.compile(".py$", re.IGNORECASE)
    filetomodule = lambda f: os.path.splitext(f)[0]
    files = filter(filere.search,
                   os.listdir(os.path.join(os.path.dirname(__file__),
                                           'parsers')))
    modulenames = sorted(map(filetomodule, files))
    modules = []

    for module in modulenames:
        if not module.startswith("__"):
            modules.append(
                importlib.import_module('dictbot.parsers.' + module))

    return modules
