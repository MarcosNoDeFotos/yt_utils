import sounddevice

from pygame import mixer, time #Playing sound


mp3 = 'F:/Documentos/scripts/binance_price_bot/static/resources/vendemos_ganancia.wav'


devs = sounddevice.query_devices()
    
devs2 = []
for dev in devs:
    if dev['max_input_channels'] != 0:
        devs2.append(dev['name'])
devs2.sort()

# mixer.init(devicename='CABLE Input (VB-Audio Virtual Cable)', channels=2) #Initialize it with the correct device
# mixer.music.load(mp3) #Load the mp3
# mixer.music.play() #Play it
# while mixer.music.get_busy(): 
#     time.Clock().tick(10)