import sounddevice

from pygame import mixer, time #Playing sound


mp3 = 'F:/Documentos/scripts/binance_price_bot/static/resources/vendemos_ganancia.wav'


devs = sounddevice.query_devices()
    
# for dev in devs:
#     dev = dev['name']
#     if dev.__contains__("Cable"):
#         print(dev)
mixer.init(devicename='CABLE Input (VB-Audio Virtual Cable)', channels=2) #Initialize it with the correct device
mixer.music.load(mp3) #Load the mp3
mixer.music.play() #Play it
while mixer.music.get_busy(): 
    time.Clock().tick(10)