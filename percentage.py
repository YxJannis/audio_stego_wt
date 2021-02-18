import sys

import matplotlib.pyplot as plt
import soundfile as sf

data_sound = sf.read("input_files/SaChenPromenade1.wav")
data_mod_sound = sf.read("output_files/wt_bit12_embedding_PCM16.wav")

try:
    start = int(sys.argv[1])
    end = int(sys.argv[2])
except:
    print("You provided no area for closer inspection. Default plot will be created!")
    start = 0
    end = 1726663

print("Running script : ", sys.argv[0])
print("Number of arguments: ", len(sys.argv))
print("You chose those arguments: ", str(sys.argv))


def percentage_wav(audio_org, audio_mod):
    percentage = []


    # getting the points
    org = audio_org[0]
    mod = audio_mod[0]

    rounds = len(org)

    org_y = []
    mod_x = []

    # get access to the y coordinates
    for i in range(rounds):
        org_y.append(org[i][0])

    for i in range(rounds):
        mod_x.append(mod[i][0])

    # calculating the percentage
    for i in range(rounds):
        if org_y[i] == 0:
            # will have an impact on the percentage
            # 2.2e-308
            org_y[i] = sys.float_info.min
        if mod_x[i] == 0:
            value = 0
        else:
            value = abs(100 - (mod_x[i] / org_y[i]) * 100)

        percentage.append(round(value))

    return percentage[start:end]


# test function to include percentage plot in dwt_plotter
def percentage_wav_2(audio_org, audio_mod):
    percentage = []

    rounds = 1726663

    # getting the points
    org_y = audio_org
    mod_x = audio_mod

    # calculating the percentage
    for i in range(rounds):
        if org_y[i] == 0:
            value = 0.0
        elif mod_x[i] == 0:
            value = 0.0
        else:
            value = abs(100 - (mod_x[i] / org_y[i]) * 100)
        percentage.append(round(value))

    return percentage


def recreate_array(percentage):
    rec_sig = []
    data_x = data_sound[1]
    data_pair = []

    for i in range(1000):
        data_pair.append(data_x[i][0])

    for x, y in zip(data_pair, percentage):
        rec_sig.extend([[x, y]])
    print('percentage array: \n')
    print(rec_sig)
    return rec_sig


if __name__ == '__main__':
    # recreate_array(percentage_audio(data, data))
    d = percentage_wav(data_sound, data_mod_sound)
    plt.title("Percentage of comparison of two signals")
    plt.ylabel("Percentage in ${0}".format(100))
    plt.plot(d)
    plt.show()
