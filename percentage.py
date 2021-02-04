import sys

from scipy.io import wavfile
import soundfile as sf
import matplotlib.pyplot as plt

audio_file_promenade_1 = "input_files/SaChenPromenade1.wav"
data = wavfile.read(audio_file_promenade_1)

audio_file_embedded = "output_files/wt_bit12_embedding_PCM16.wav"
data_mod = wavfile.read(audio_file_embedded)

data_sound = sf.read("input_files/SaChenPromenade1.wav")
data_mod_sound = sf.read("output_files/wt_bit12_embedding_PCM16.wav")


def percentage_wav(audio_org, audio_mod, file_type):
    percentage = []

    rounds = 1726663

    # getting the points
    if file_type == "wav":
        org = audio_org[1]
        mod = audio_mod[1]
    else:
        org = audio_org[0]
        mod = audio_mod[0]

    org_y = []
    mod_x = []

    # get access to the y coordinates
    for i in range(rounds):
        for j in range(1):
            org_y.append(org[i][1])

    for i in range(rounds):
        for j in range(1):
            mod_x.append(mod[i][1])

    # calculating the percentage
    for i in range(rounds):
        if org_y[i] == 0:
            # will have an impact on the percentage
            # 2.2e-308
            org_y[i] = sys.float_info.min
        if mod_x[i] == 0:
            value = 0
        else:
            value = 100 - (mod_x[i] / org_y[i]) * 100

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


# recreate_array(percentage_audio(data, data))
d = percentage_wav(data_sound, data_mod_sound, "sound")
plt.plot(d)
plt.show()
