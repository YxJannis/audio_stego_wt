from audio_file import AudioFile
import soundfile

file_path = 'testdata/44 Pianisten 02-Der Zwerg.wav'
signal_data, sampling_rate = soundfile.read(file_path, dtype='int16')
out_file = 'testdata/out_der_Zwerg.wav'


suspicious_elements = []
threshold = 1000

new_signal = signal_data.copy()

for i in range(2, len(signal_data)-1):
    # if difference between data[i-1], data [i] und data[i+1], data[i] zu groß erstmal elemente at i, i+1, i-1 ausgeben
    x_0 = signal_data[i-1]
    x_1 = signal_data[i]
    x_2 = signal_data[i+1]
    if (x_1 > x_0 and x_1 > x_2) or (x_1 < x_0 and x_1 < x_2):
        if abs(x_1)-abs(x_0) > threshold or abs(x_2)-abs(x_0) > threshold:
            print(f'{x_0}, {x_1}, {x_2}')
            suspicious_elements.append(i)
            new_signal[i] = (x_0 + x_2)/2

modified = []
for j in range(1, len(signal_data)):
    if new_signal[j] != signal_data[j]:
        print(f'Changed from: {signal_data[j]} to {new_signal[j]}')
        modified.append(j)

soundfile.write(out_file, new_signal, sampling_rate, subtype='PCM_16')
# print(f'{suspicious_elements}')
