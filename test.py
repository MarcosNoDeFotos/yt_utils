import wave
import utils
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

wav_obj = wave.open(utils.currentPath+'audio_out/30-04-2024-011452/micro.wav', 'rb')
wav_obj2 = wave.open(utils.currentPath+'audio_out/30-04-2024-011452/escritorio2.wav', 'rb')


n_samples = wav_obj.getnframes()
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


treshold = 100
reduccion_a = 100
l_channel = list(l_channel)
l_channel_2 = list(l_channel_2)
# for index, frame in enumerate(tqdm(l_channel)):
#     if frame<0 and frame<-treshold:
#         if l_channel_2[index]<frame:
#             l_channel_2[index] = reduccion_a
#     elif frame>0 and frame>treshold:   
#         if l_channel_2[index]>frame:
#             l_channel_2[index] = reduccion_a


plt.figure(figsize=(15, 5))
plt.plot(times, l_channel)

# plt.plot(times_2, l_channel_2)
plt.title('Left Channel')
plt.ylabel('Signal Value')
plt.xlabel('Time (s)')
plt.xlim(0, t_audio)
plt.show()
