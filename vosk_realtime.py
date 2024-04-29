from typing import Iterable
from vosk import Model, KaldiRecognizer
import pyaudio
import json
from utils import *
import multiprocessing
from soundsRecognition import *
import importlib.machinery
import importlib.util
import os
from time import sleep
from _thread import start_new_thread

class VoskVoiceRecognitionToText(multiprocessing.Process):
    
    
    def __init__(self,):
        multiprocessing.Process.__init__(self)
        self.exit = multiprocessing.Event()
        
    def run(self):
        
        model = Model(currentPath+"vosk-model-small-es-0.42")
        recognizer = KaldiRecognizer(model, 128000)
        mic = pyaudio.PyAudio()
        stream = mic.open(format=pyaudio.paInt16, channels=1, rate=128000, input=True, frames_per_buffer=1024,)
        stream.start_stream()
        with open(currentPath+f"out-{getFechaHora()}.txt", "a", encoding="utf-8") as out:
            try:
                while not self.exit.is_set():
                    try:
                        try:
                            data = stream.read(1024)
                            # if not recognizer.AcceptWaveform(data):
                            #     text = json.loads(recognizer.PartialResult())
                            #     if text["partial"] != None:
                            #         textClean = str(text["partial"]).strip()
                            #         # print(f"{textClean} {textClean != lastText} {not textClean and textClean != lastText}");
                            #         if (not textClean and textClean != lastText) or not lastText:
                            #             lastText = textClean
                            #             if textClean != "":
                            #                 fullText += textClean+"\n"
                            #         print(textClean);
                            # else:
                            #     text = json.loads(recognizer.Result())
                            #     textClean = "FULL_ "+str(text["text"]).strip();
                            # print(textClean)
                            if recognizer.AcceptWaveform(data):
                                text = json.loads(recognizer.Result())
                                textClean = str(text["text"]).strip();
                                if textClean:
                                    out.write(textClean)
                        except Exception as e1:
                            print(e1)
                            print(text)
                    except Exception as e2:
                        print(e2)
            except Exception as e:
                print(e)
            
            out.close()
            print("Fin grabación")
    
    def terminate(self):
        self.exit.set()




class VoskVoiceRecognitionPlaySound(multiprocessing.Process):
    

    soundsPlayerModules = []
    soundsModulesPath = currentPath+"soundsRecognition/"
    playing = False
    def __init__(self,):
        multiprocessing.Process.__init__(self)
        self.exit = multiprocessing.Event()
        
    def run(self):
        for moduleName in os.listdir(self.soundsModulesPath):
            if moduleName.endswith(".py"):
                loader = importlib.machinery.SourceFileLoader( moduleName, self.soundsModulesPath+moduleName )
                spec = importlib.util.spec_from_loader( moduleName, loader )
                module = importlib.util.module_from_spec( spec )
                loader.exec_module( module )
                self.soundsPlayerModules.append(module)
        model = Model(currentPath+"vosk-model-small-es-0.42")
        recognizer = KaldiRecognizer(model, 128000)
        mic = pyaudio.PyAudio()
        stream = mic.open(format=pyaudio.paInt16, channels=1, rate=128000, input=True, frames_per_buffer=4096,)
        stream.start_stream()
        lastText = None
        lastTextPlayed = ''
        try:
            while not self.exit.is_set():
                try:
                    try:
                        data = stream.read(4096)
                        textDetected = None
                        if not recognizer.AcceptWaveform(data):
                            text = json.loads(recognizer.PartialResult())
                            text = str(text["partial"]).strip()
                            # print(f"{lastText}                     {text}")
                            if not lastTextPlayed.__contains__(text):
                                textDetected = lastText
                            lastText = text
                        else:
                            text = json.loads(recognizer.Result())
                        #     text = str(text["text"]).strip()
                        #     if text and text != '' and text != lastText:
                        #         lastText = text
                        #         textDetected = text
                        if  textDetected and textDetected != '' and not self.playing and not lastTextPlayed.__contains__(textDetected):
                            
                            print(textDetected)
                            for module in self.soundsPlayerModules:
                                # print(module.playing)
                                if module.canPlay(clearText(textDetected)):
                                    recognizer.Result()
                                    recognizer.Reset()
                                    self.playing = True
                                    lastTextPlayed = textDetected
                                    start_new_thread(self.th_resetPlaying,())
                                    module.playSound(clearText(textDetected))
                                else:
                                    lastTextPlayed = ''
                                
                            textDetected = None

                    except Exception as e1:
                        print(e1)
                except Exception as e2:
                    print(e2)
        except Exception as e:
            print(e)
    def th_resetPlaying(self):
        sleep(2)
        self.playing = False
    def terminate(self):
        self.exit.set()