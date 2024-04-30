from datetime import datetime
import unicodedata
import os
from shutil import move, rmtree
import requests
import zipfile
from multiprocessing import Process

currentPath = __file__.replace(__file__.split("\\")[-1], "").replace("\\", "/")
ffmpegPath = currentPath+"bin/ffmpeg/"

ffmpegDownloadURL ="https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"




def getFechaHora():
    return datetime.now().strftime("%d-%m-%Y-%H%M%S")


def clearText(text:str):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')


def download_file(url, filename):
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    f.write(chunk)
        return filename
    except:
        return None

def downloadFFMPEG():

    if not os.path.exists(ffmpegPath):
        try:
            downloadPath = ffmpegPath+"temp"
            os.makedirs(downloadPath)
            print("Descargando FFMPEG...")
            ffmpegZIPFIle = download_file(ffmpegDownloadURL, downloadPath+"/ffmpeg.zip");
            if ffmpegDownloadURL:
                print("Descomprimiendo FFMPEG...")
                with zipfile.ZipFile(ffmpegZIPFIle, 'r') as zip_ref:
                    zip_ref.extractall(downloadPath)
                move(downloadPath+"/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe", ffmpegPath)
                rmtree(downloadPath)
                print("FFMPEG Descargado correctamente")
        except Exception as e:
            print(e)

if __name__ == '__main__':
    Process(target=downloadFFMPEG).start()