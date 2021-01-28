from audio_file import AudioFile

audio = AudioFile('')
audio_data = audio.signal_data.T[0]

print(f'{audio_data}\n\n{audio_data[0]}\n\n{audio_data.T}\n\n{audio_data.T[0]}')

count = 0


for i in range(2, len(audio_data)):
    # if difference between data[i-1], data [i] und data[i+1], data[i] zu groß erstmal elemente at i, i+1, i-1 ausgeben
    # TODO: threshold ausprobieren
    # TODO: wie messen? nur difference zwischen i-1 und i / i+1 und i oder schauen ob die diff between 
    prev_c = audio_data[i-1]
    curr_c = audio_data[i]
    next_c = audio_data[i+1]
