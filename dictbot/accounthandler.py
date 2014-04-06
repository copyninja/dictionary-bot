import sleekxmpp
from dictbot.pluginloader import load_plugins
from dictbot.replyhandler import ReplyMessage
from dictbot.langstrings import welcome_strings, notfound_strings
from dictbot.wiktionary import WiktionaryPageNotFoundError

PLUGINS = load_plugins()


class JabberAccount(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password, lang, plugins):
        super(JabberAccount, self).__init__(jid, password)
        self._dictbot_plugins = plugins
        self._lang = lang
        self._send_reply = self.process_meanings()

        for module in PLUGINS:
            if module.get_supported_lang() == self._lang:
                self._parser = module

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)

        self.set_authorize = True

    def _handle_commands(self, command, to, subject, type):
        if command == ":help":
            self.make_message(to, welcome_strings[self._lang],
                              "Re: " + subject, type).send()

    def session_start(self, event):
        self.send_presence()
        self.get_roster()
        self._send_reply.send(None)

    def _process_meanings(self):
        reply_msg = ReplyMessage()
        while True:
            try:
                meanings, to, subject, type = (yield)
                reply, reply_html = reply_msg.prepare_meaning_reply(meanings)
                self.make_message(to, reply,
                                  "Re: " + subject, type, reply_html).send()
            except GeneratorExit:
                pass

    def message(self, message):
        type = message['type']
        body = message['body']
        subject = message['subject']
        to = message['from']

        if type in ['chat', 'normal']:
            if body.startswith(":"):
                self._handle_commands(body, to, subject, type)
            else:
                words = body.split(' ')
                for word in words:
                    try:
                        meanings = self._parser.get_meaning(word)
                        self._send_reply.send((meanings, to, subject, type))
                    except WiktionaryPageNotFoundError:
                        self.make_message(to, notfound_strings[self._lang],
                                          "Re: " + subject, type).send()
                        pass
                    except Exception:
                        # TODO something else went wrong log it
                        pass
        # Close generator
        self._send_reply.close()
