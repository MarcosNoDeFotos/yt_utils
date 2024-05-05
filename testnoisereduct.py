from scipy.io import wavfile
import utils
import noisereduce as nr
# load data
# perform noise reduction


rate, data = wavfile.read(utils.currentPath+'audio_out/30-04-2024-011452/micro.wav', 'rb')


reduced_noise = nr.reduce_noise(y=data, sr=rate, chunk_size=30)
wavfile.write(utils.currentPath+'audio_out/30-04-2024-011452/micro_reduced.wav', rate, reduced_noise)