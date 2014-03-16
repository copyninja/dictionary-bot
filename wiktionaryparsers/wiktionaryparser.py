
class WiktionaryParser:
    def __init__(self, logger):
        self.xhtml_im_header = """
<html xmlns='http://jabber.org/protocol/xhtml-im'>
  <body xmlns='http://www.w3.org/1999/xhtml'>
"""
        self.xhtml_im_footer = """
  </body>
</html>
"""
        self.logger = logger

    def get_meaning(self, data):
        pass
