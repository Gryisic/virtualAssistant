from Scripts.Front.main_window import MainWindow
from Scripts.Back.recognizer import Recognizer

from pathlib import Path

model_path = Path.cwd().joinpath('LocalData\\models\\Mistral')


def main():
    model_path.mkdir(parents=True, exist_ok=True)
    #window = MainWindow(recognizer=Recognizer())
    #window.create()


if __name__ == '__main__':
    main()
