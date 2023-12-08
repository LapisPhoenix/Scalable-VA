import time
import ai
from ext.command import Command


class TimeCMD(Command):
    def __init__(self, keyword: str, voice_assistant: ai.VoiceAssistant):
        self.keyword = keyword
        self.voice_assistant = voice_assistant
        super().__init__(self.keyword, self.voice_assistant)

    def run_command(self):
        current_time = time.strftime('%I:%M %p')
        self.voice_assistant.speak(f'The time is {current_time}')


def load(voice_assistant):
    return TimeCMD('time', voice_assistant)
