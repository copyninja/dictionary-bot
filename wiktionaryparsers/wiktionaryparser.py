from xml.etree import cElementTree as ET


class WiktionaryParser:
    __slots__ = ["meanings", "xhtml_im_header", "xhtml_im_footer",
                 "logger"]

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

    def prepare_message(self):
        if len(self.meanings) > 0:
            reply_body = ''
            reply_xml = self.xhtml_im_header

            # some time wiktionary does not contain word type
            # i.e. verb noun etc. Process the below only if its present
            if len(self.meanings.get('wtypes')) > 0:
                i = 0
                for wtype in self.meanings.get('wtypes'):
                    reply_body += '\n' + wtype + ': \n'
                    reply_xml += '<br/><strong>' + wtype + ': </strong><br/>'

                    defs = ','.join(self.meanings.get('definitions')[i])
                    reply_body += defs
                    reply_xml += '<p>' + defs + '</p>'

                    i += 1
            else:
                defs = ','.join(self.meanings.get('definitions')[0])
                reply_body += defs
                reply_xml = '<p>' + defs + '</p>'

            reply_xml += self.xhtml_im_footer
            ctree = ET.fromstring(reply_xml)
            if len(reply_body) > 0:
                return (reply_body, ctree)
