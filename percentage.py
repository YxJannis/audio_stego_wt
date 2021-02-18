import sys

import matplotlib.pyplot as plt
import soundfile as sf

data_sound, f = sf.read("input_files/SaChenPromenade1.wav")
data_mod_sound, f = sf.read("output_files/wt_bit12_embedding_PCM16.wav")

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

    rounds = len(audio_org)

    # getting the points
    org = audio_org
    mod = audio_mod

    # calculating the percentage
    for i in range(rounds):
        if org[i] == 0:
            value = 0.0     # cant calculate percentage increase from 0
        elif mod[i] == 0:
            value = 1    # if modified coefficient is 0, the change to coefficient is 100%
        else:
            # value = abs(100 - (mod_x[i] / org_y[i]) * 100)
            value = abs((1-mod[i]/org[i]))
        percentage.append(value)

    return percentage[start:end]


# test function to include percentage plot in dwt_plotter
def percentage_wav_2(audio_org, audio_mod):
    percentage = []

    rounds = len(audio_org)

    # getting the points
    org = audio_org
    mod = audio_mod

    # calculating the percentage
    for i in range(rounds):
        if org[i] == 0:
            value = 0.0     # cant calculate percentage increase from 0
        elif mod[i] == 0:
            value = 1     # if modified coefficient is 0, the change to coefficient is 100%
        else:
            # value = abs(100 - (mod_x[i] / org_y[i]) * 100)
            value = abs((1-mod[i]/org[i]))
        percentage.append(value)

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
    d = percentage_wav(data_sound.T[0], data_mod_sound.T[0])
    plt.title("Percentage of comparison of two signals")
    plt.ylabel("Percentage")
    plt.plot(d)
    plt.savefig(f'plot_images/percentage')
    plt.show()
