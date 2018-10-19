from mycroft import MycroftSkill, intent_file_handler


class PicroftGoogleAiyVoicehat(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('voicehat.aiy.google.picroft.intent')
    def handle_voicehat_aiy_google_picroft(self, message):
        self.speak_dialog('voicehat.aiy.google.picroft')


def create_skill():
    return PicroftGoogleAiyVoicehat()

