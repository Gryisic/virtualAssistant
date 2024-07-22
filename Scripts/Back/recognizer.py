import time
import speech_recognition

from Scripts.Back.Logs import recognition_logs
from Scripts.Back.Commands import commands
from Scripts.Back.Commands.Objects.Speaker.speaker import speak
from Scripts.Utils.events_handler import register_handler


class Recognizer:
    logs = recognition_logs.RecognitionLogs()
    recognizer = speech_recognition.Recognizer()
    is_active = False
    stop = None

    def __init__(self):
        register_handler('stop_recognition', self.stop_listening)

    def listen(self):
        speak("Я слушаю!")

        def callback(recognizer, audio):
            try:
                query = recognizer.recognize_google(audio, language='ru-RU').lower()
                self.logs.add(query)
                commands.process(query)
            except speech_recognition.UnknownValueError:
                pass

        microphone = speech_recognition.Microphone(device_index=4)
        with microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)

        self.stop = self.recognizer.listen_in_background(microphone, callback)

        while self.is_active:
            time.sleep(0.1)

        speak('Я спать!')

    def start_listening(self):
        self.is_active = True
        self.listen()

    def stop_listening(self):
        self.is_active = False
        self.stop(wait_for_stop=False)
