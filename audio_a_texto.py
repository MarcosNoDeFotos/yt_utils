#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu
from audio_a_textoui import AudioTextoUI


class AudioTexto(AudioTextoUI):
    def __init__(self, master=None):
        super().__init__(master)


if __name__ == "__main__":
    app = AudioTexto()
    app.run()
