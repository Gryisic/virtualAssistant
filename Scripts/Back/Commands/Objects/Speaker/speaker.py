from io import BytesIO
from gtts import gTTS

import pyglet
import threading

pyglet.options["audio"] = ("directsound",)


def speak(words: str, language: str = 'ru'):
    def threaded_speak():
        with BytesIO() as f:
            gTTS(text=words, lang=language).write_to_fp(f)
            f.seek(0)

            player = pyglet.media.load("_.mp3", file=f).play()
            while player.playing:
                pyglet.app.platform_event_loop.dispatch_posted_events()
                pyglet.clock.tick()

    thread = threading.Thread(target=threaded_speak, daemon=True)
    thread.start()
