import wave
import utils
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

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
plt.figure(1)
plt.subplot(211)
plt.plot(times, l_channel)
plt.xlim(0, t_audio)
plt.subplot(212)
plt.plot(times, new_channel_l)
plt.xlim(0, t_audio)
plt.show()
