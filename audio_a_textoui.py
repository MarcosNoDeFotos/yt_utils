#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu
import multiprocessing as mp
from vosk_realtime import VoskVoiceRecognitionToText, VoskVoiceRecognitionPlaySound
PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "prjGUI.ui"
RESOURCE_PATHS = [PROJECT_PATH]



class AudioTextoUI:
    vosk = None
    initialTexts = {}
    recording = False
    def __init__(self, master=None):
        self.builder = pygubu.Builder()
        self.builder.add_resource_paths(RESOURCE_PATHS)
        self.builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow: tk.Tk = self.builder.get_object("tk1", master)
        self.builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()

    def _reproducirSonido(self, widget_id:str):
        widget_id = widget_id.lower()
        button = self.mainwindow.children[widget_id]
        if not self.recording:
            self.vosk = VoskVoiceRecognitionPlaySound()
            if not self.initialTexts.__contains__(widget_id):
                self.initialTexts[widget_id] = button["text"];
            self.vosk.start()
            button["text"] = "Parar"
            self.recording = True
        else:
            self.vosk.terminate()
            button["text"] = self.initialTexts[widget_id]
            self.recording = False

    def _reconocerYGuardar(self, widget_id:str):
        widget_id = widget_id.lower()
        button = self.mainwindow.children[widget_id]
        if not self.recording:
            self.vosk = VoskVoiceRecognitionToText()
            if not self.initialTexts.__contains__(widget_id):
                self.initialTexts[widget_id] = button["text"];
            self.vosk.start()
            button["text"] = "Parar"
            self.recording = True
        else:
            self.vosk.terminate()
            button["text"] = self.initialTexts[widget_id]
            self.recording = False
            
            
        



if __name__ == "__main__":
    app = AudioTextoUI()
    app.run()
