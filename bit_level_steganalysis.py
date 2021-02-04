from audio_file import AudioFile
import soundfile


def interpolate_outliers(in_path, out_path):
    signal_data, sampling_rate = soundfile.read(in_path, dtype='int16')
    new_signal = signal_data.copy()

    suspicious_elements = []
    threshold = 1000
    for i in range(2, len(signal_data)-1):
        x_0 = signal_data[i-1]
        x_1 = signal_data[i]
        x_2 = signal_data[i+1]
        if (x_1 > x_0 and x_1 > x_2) or (x_1 < x_0 and x_1 < x_2):
            if abs(x_1)-abs(x_0) > threshold or abs(x_2)-abs(x_0) > threshold:
                # print(f'{x_0}, {x_1}, {x_2}')
                suspicious_elements.append(i)
                new_signal[i] = (x_0 + x_2)/2
    modified = []
    for j in range(1, len(signal_data)):
        if new_signal[j] != signal_data[j]:
            print(f'Changed from: {signal_data[j]} to {new_signal[j]}')
            modified.append(j)

    soundfile.write(out_path, new_signal, sampling_rate, subtype='PCM_16')


def interpolate_all(in_path, out_path):
    signal_data, sampling_rate = soundfile.read(in_path, dtype='int16')
    new_signal = signal_data.copy()

    for i in range(2, len(signal_data)-1):
        x_0 = signal_data[i-1]
        x_1 = signal_data[i]
        x_2 = signal_data[i+1]
        new_signal[i] = (x_0+x_2)/2

    soundfile.write(out_path, new_signal, sampling_rate, subtype='PCM_16')


if __name__ == '__main__':
    # interpolate_outliers('testdata/44 Pianisten 01-Promenade.wav', 'testdata/interp_outliers_Pianisten_Promenade.wav')
    # interpolate_outliers('testdata/44 Pianisten 02-Der Zwerg.wav', 'testdata/interp_outliers_Pianisten_Zwerg.wav')
    interpolate_outliers('testdata/Sa Chen 1. Promenade.wav', 'testdata/interp_outliers_SaChen_1Promenade.wav')
    interpolate_outliers('testdata/Sa Chen 2. Gnomus.wav', 'testdata/interp_outliers_SaChen_Gnomus.wav')
    # interpolate_all('testdata/44 Pianisten 01-Promenade.wav', 'testdata/interp_all_Pianisten_Promenade.wav')
    # interpolate_all('testdata/44 Pianisten 02-Der Zwerg.wav', 'testdata/interp_all_Pianisten_Zwerg.wav')
    interpolate_all('testdata/Sa Chen 1. Promenade.wav', 'testdata/interp_all_SaChen_1Promenade.wav')
    interpolate_all('testdata/Sa Chen 2. Gnomus.wav', 'testdata/interp_all_SaChen_Gnomus.wav')
