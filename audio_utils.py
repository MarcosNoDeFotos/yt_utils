from tkinter.filedialog import askopenfilenames
from subprocess import call
from utils import *

extraerTodosCanalesMezclados = False
fileTypesToOpen = [
    ("*.mp4", "Archivos de vídeo mp4")
]


def dividirVideoEnAudios(video_path:str):
    out_canales = currentPath+"audio_out/"+getFechaHora()+"/"
    os.makedirs(out_canales)
    print("Extrayendo canales...")
    if extraerTodosCanalesMezclados:
        returnCode = call([ffmpegPath+"ffmpeg.exe", "-stats", "-v", "quiet", "-i", f"{video_path}", "-map", "0:a:0", "-c", "copy", f"{out_canales}todo.aac", "-map", "0:a:1", "-c", "copy", f"{out_canales}escritorio.aac", "-map", "0:a:2", "-c", "copy", f"{out_canales}micro.aac", "-map", "0:a:3", "-c", "copy", f"{out_canales}discord.aac"])
    else:
        returnCode = call([ffmpegPath+"ffmpeg.exe", "-stats", "-v", "quiet", "-i", f"{video_path}", "-map", "0:a:1", "-c", "copy", f"{out_canales}escritorio.aac", "-map", "0:a:2", "-c", "copy", f"{out_canales}micro.aac", "-map", "0:a:3", "-c", "copy", f"{out_canales}discord.aac"])
    if returnCode == 0:
        print("Se extraen los canales de "+video_path)
        for aac in os.listdir(out_canales):
            if aac.endswith(".aac"):
                newFilename = out_canales+aac.replace(".aac", ".wav")
                returnCode = call([ffmpegPath+"ffmpeg.exe", "-v", "quiet", '-i', out_canales+aac, newFilename])
                if returnCode == 0:
                    print("\tSe convierte a wav "+aac)
                    os.remove(out_canales+aac)
                else:
                    print("Error al convertir a wav "+aac)
    else:
        print("Error al extraer canales de "+video_path)


videos_to_process = askopenfilenames(filetypes=fileTypesToOpen, title="Seleccionar un vídeo para dividir canales")

for video_path in videos_to_process:
    dividirVideoEnAudios(video_path)



