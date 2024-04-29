#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu
from YT_Utilsui import YT_UtilsUI


class YT_Utils(YT_UtilsUI):
    def __init__(self, master=None):
        super().__init__(master)

    def _reproducirSonido(self, widget_id):
        pass

    def _reconocerYGuardar(self, widget_id):
        pass

    def _traducirPantalla(self, widget_id):
        pass


if __name__ == "__main__":
    app = YT_Utils()
    app.run()
