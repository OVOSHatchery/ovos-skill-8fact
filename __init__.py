from mycroft.skills.core import FallbackSkill, intent_file_handler, \
    intent_handler
import py8fact
from mtranslate import translate
from os.path import join, dirname


class FactsSkill(FallbackSkill):
    def __init__(self):
        super().__init__(name='8FactSkill')

    def get_intro_message(self):
        # welcome dialog on skill install
        self.speak_dialog("intro", {"skill_name":"8 fact"})

    @intent_file_handler("random_fact.intent")
    def handle_random_fact(self, message):
        lang = self.lang.split("-")[0]
        fact = py8fact.random_fact(lang)
        if lang not in py8fact.SUPPORTED_LANGS:
            fact = translate(fact, self.lang)
        self.gui.show_text(fact)
        self.speak(fact, wait=True)
        self.gui.clear()

    @intent_file_handler("number_facts.intent")
    def handle_num_fact(self, message):
        n = py8fact.total_facts()
        self.speak_dialog("number_facts", {"number": n})

    @intent_file_handler("trustworthy.intent")
    def handle_trustworthy(self, message):
        self.speak_dialog("no_idea")

    @intent_file_handler("source.intent")
    def handle_source(self, message):
        self.gui.show_image(join(dirname(__file__), "logo.jpg"),
                            caption="Take all info with a grain of salt",
                            fill='PreserveAspectFit')
        self.speak_dialog("8fact", wait=True)
        self.gui.clear()


def create_skill():
    return FactsSkill()
