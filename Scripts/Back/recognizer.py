import speech_recognition
from Scripts.Back.Commands import commands

from Scripts.Back.Commands.Objects.Speaker.speaker import speak

recognizer = speech_recognition.Recognizer()

def listen():
    speak("Я слушаю!")

    try:
        with speech_recognition.Microphone(device_index=4) as microphone:
            recognizer.adjust_for_ambient_noise(source=microphone, duration=0.5)
            audio = recognizer.listen(microphone)
            query = recognizer.recognize_google(audio_data=audio, language='ru-RU').lower()

            commands.process(query)

    except speech_recognition.UnknownValueError:
        speak('Я не поняла!')