import ai
import abc


class Command(abc.ABC):
    def __init__(self, keyword: str, voice_assistant: 'ai.VoiceAssistant'):
        self.keyword = keyword
        self.voice_assistant = voice_assistant

    @abc.abstractmethod
    def run_command(self):
        pass