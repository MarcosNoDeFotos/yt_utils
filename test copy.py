import wave
import utils
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from pydub import AudioSegment
amplitudOnda = 500



#Pintamos la onda de volumen de un wav


wav_obj = wave.open(utils.currentPath+'audio_out/30-04-2024-011452/micro.wav', 'rb')
wav_obj2 = wave.open(utils.currentPath+'audio_out/30-04-2024-011452/escritorio2.wav', 'rb')


n_samples = 30000#wav_obj.getnframes()
sample_freq = wav_obj.getframerate()
signal_wave = wav_obj.readframes(n_samples)

signal_array = np.frombuffer(signal_wave, dtype=np.int16)
l_channel = signal_array[0::2]
r_channel = signal_array[1::2]
times = np.linspace(0, n_samples/sample_freq, num=n_samples)
t_audio = n_samples/sample_freq

n_samples_2 = n_samples#wav_obj.getnframes()
sample_freq_2 = wav_obj2.getframerate()
signal_wave_2 = wav_obj2.readframes(n_samples_2)

signal_array_2 = np.frombuffer(signal_wave_2, dtype=np.int16)
l_channel_2 = signal_array_2[0::2]
r_channel_2 = signal_array_2[1::2]
times_2 = np.linspace(0, n_samples_2/sample_freq_2, num=n_samples_2)
t_audio_2 = n_samples_2/sample_freq_2


treshold = 900
reduccion_a = 400
l_channel = list(l_channel)
l_channel_2_original = list(l_channel_2)
l_channel_2 = list(l_channel_2)





treshold_finder = []
for i in range(0, l_channel.__len__()):
    if i%2==0:
        treshold_finder.append(treshold)
    else:
        treshold_finder.append(-treshold)





new_channel_l = [];
scalex = []
ascending = l_channel[1] > l_channel[0]
for index, frame in enumerate(tqdm(l_channel)):
    if index+1<l_channel.__len__():
        if ascending and l_channel[index+1] < frame:
            ascending = False
            new_channel_l.append(frame)
            scalex.append(index)
        elif not ascending and l_channel[index+1] > frame:
            ascending = True
            new_channel_l.append(frame)
            scalex.append(index)
        else:
            new_channel_l.append(0)
    else:
        new_channel_l.append(0)



indexComienzaAHablar = -1
hablando = False
cortes = [0]
for index, frame in enumerate(tqdm(l_channel)):
    if (frame <0 and frame <= -treshold) or (frame >0 and frame >= treshold): # Si supera el mínimo del umbral
        
        if not hablando:
            hablando = True
            indexComienzaAHablar = index
            for i in range(index, index+10):
                if i%2==0:
                    treshold_finder[i] = 30000
                else:
                    treshold_finder[i] = -30000
    else:
        if hablando and indexComienzaAHablar+5000 <=index:
            if index+10 <= l_channel.__len__():
                cortes.append(index/sample_freq_2)
                for i in range(index, index+10):
                    if i%2==0:
                        treshold_finder[i] = 30000
                    else:
                        treshold_finder[i] = -30000
            hablando = False
cortes.append(t_audio)

print(cortes)
print(cortes.__len__())
originalAudio = AudioSegment.from_wav(utils.currentPath+'audio_out/30-04-2024-011452/micro.wav')
for i, corte in enumerate(cortes):
    if i+1<cortes.__len__():
        corteFrom = corte*1000
        corteTo = cortes[i+1]*1000
        newAudio = originalAudio[corteFrom:corteTo]
        newAudio.export(utils.currentPath+f'audio_out/30-04-2024-011452/SPLIT{i+1}.wav', format="wav") #Exports to a wav file in the current path
        print(f"{corte} - {cortes[i+1]}")

plt.figure(1)
plt.subplot(211)
plt.plot(times, l_channel)
plt.xlim(0, t_audio)
plt.subplot(212)
plt.plot(times, new_channel_l)
plt.plot(times_2, treshold_finder, color=(.0, 0.0, 1.0, .8))
plt.xlim(0, t_audio)
plt.show()
