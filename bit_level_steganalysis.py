from audio_file import AudioFile

audio = AudioFile('testdata/44 Pianisten 01-Promenade.wav')
audio_data = audio.signal_data

size = len(audio_data)


count = 0
suspicious_elements = []
threshold = 0.18


for i in range(2, len(audio_data)-1):
    # if difference between data[i-1], data [i] und data[i+1], data[i] zu groß erstmal elemente at i, i+1, i-1 ausgeben
    # TODO: threshold ausprobieren
    # TODO: wie messen? nur difference zwischen i-1 und i / i+1 und i oder schauen ob die diff between
    x_0 = audio_data[i-1]
    x_1 = audio_data[i]
    x_2 = audio_data[i+1]
    if (abs(x_1) - (abs(x_0) - abs(x_2))) > threshold:
        print(f'{x_0}, {x_1}, {x_2}')
        suspicious_elements.append(i)


print(f'{suspicious_elements}')
