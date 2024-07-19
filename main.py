from Scripts.Front.main_window import MainWindow
from Scripts.Back.recognizer import Recognizer

import asyncio


def main():
    window = MainWindow(recognizer=Recognizer())
    window.create()


if __name__ == '__main__':
    main()
