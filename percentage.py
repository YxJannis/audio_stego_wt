from scipy.io import wavfile
import numpy as np

audio_file_promenade_1 = "input_files/SaChenPromenade1.wav"
data = wavfile.read(audio_file_promenade_1)


def percentage_audio(audio_org, audio_mod):
    percentage = []

    # getting the points
    org = audio_org[1]
    mod = audio_mod[1]
    org_y = []
    mod_x = []

    # get access to the y coordinates
    for i in range(1000):
        for j in range(1):
            org_y.append(org[i][1])

    for i in range(1000):
        for j in range(1):
            mod_x.append(mod[i][1])

    # calculating the percentage
    for i in range(1000):
        if org_y[i] == 0:
            org_y[i] = 0.00000000000000001
        value = (mod_x[i]/org_y[i]) * 100
        percentage.append(value)
    return percentage


def recreate_array(percentage):
    rec_sig = []
    data_x = data[1]
    data_pair = []
    
    for i in range(1000):
        for j in range(1):
            data_pair.append(data_x[i][0])

    for x, y in zip(data_pair, percentage):
        rec_sig.extend([[x, y]])
    print('percentage array: \n')
    print(rec_sig)
    return rec_sig


recreate_array(percentage_audio(data, data))
