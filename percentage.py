from scipy.io import wavfile


def percentage_audio(audio_org, audio_mod):
    percentage = []

    # getting the points
    org = audio_org[1]
    mod = audio_mod[1]
    org_y = []
    mod_x = []

    # get access to the y coordinates
    for i in range(1726662):
        for j in range(1):
            org_y.append(org[i][0])

    for i in range(1726662):
        for j in range(1):
            mod_x.append(mod[1][0])

    # calculating the percentage
    for i in range(1726662):
        if org_y[i] == 0:
            percentage.insert(0, [i])
        percentage.append((mod_x[i] / org_y[i]) * 100)
    print(percentage)
    return percentage


audio_file_promenade_1 = "input_files/SaChenPromenade1.wav"
data = wavfile.read(audio_file_promenade_1)
percentage_audio(data, data)
