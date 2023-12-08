import importlib.util
import threading
import vosk
import pyttsx3
import speech_recognition as sr
from ext.command import Command

DEFAULT_NAME = 'Voice Assistant'
DEFAULT_ACTIVATION_KEYWORD = 'computer'
DEFAULT_RATE = 150
DEFAULT_VOLUME = 0.9
DEFAULT_VOICE = 'english-us'
FAIL_RESPONSE = "Sorry, I didn't get that."


class VoiceAssistant:
    def __init__(self, name: str | None = None, activation_keyword: str | None = None):
        """
        Initialize a VoiceAssistant object.

        :param name: (str | None, optional) The name of the voice assistant. Defaults to 'Voice Assistant'.
        :param activation_keyword: (str | None, optional) The activation keyword for the voice assistant. Defaults to 'computer'.   # noqa
        """
        self.name = name or DEFAULT_NAME
        self.activation_keyword = activation_keyword or DEFAULT_ACTIVATION_KEYWORD

        self.set_up_engine()

        self.commands = {}  # {keyword: callback}

        vosk.SetLogLevel(-1)  # To disable logs from vosk

    def set_up_engine(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', DEFAULT_RATE)
        self.engine.setProperty('volume', DEFAULT_VOLUME)
        self.engine.setProperty('voice', DEFAULT_VOICE)

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def load_command(self, path: str):
        spec = importlib.util.spec_from_file_location("module.name", path)
        command_instance = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(command_instance)
        instance = command_instance.load(self)  # load instance from command module
        self.add_command(instance)

    def add_command(self, command: Command):
        self.commands[command.keyword] = command.run_command

    def listen_and_process_command(self):
        while True:
            text = self._listen()
            if text and self._check_for_activation(text):
                self.speak("How can I help you?")
                result_text = self._listen()
                if result_text:
                    self._process_command(result_text)
                else:
                    self.speak(FAIL_RESPONSE)

    @staticmethod
    def _listen():
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.pause_threshold = 1
            audio = r.listen(source)

        try:
            query = r.recognize_vosk(audio, language='en-in')
            return query

        except Exception:  # noqa
            return None

    def _check_for_activation(self, text: str) -> bool:
        return self.activation_keyword in text.lower()

    def _process_command(self, text: str):
        for keyword, command in self.commands.items():
            if keyword in text.lower():
                command()

    def _run(self):
        threading.Thread(target=self.run, daemon=True).start()

    def run(self):
        self.speak(f"{self.name} online! Activate me with: '{self.activation_keyword}'.")  # noqa
        self.listen_and_process_command()
