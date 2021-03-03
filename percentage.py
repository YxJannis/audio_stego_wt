import sys

import matplotlib.pyplot as plt
import soundfile as sf

data_sound, f = sf.read("input_files/orig/44 Pianisten 01-Promenade.wav")
data_mod_sound, f = sf.read("output_files/mod/44 Pianisten 01-Promenade.wav")

try:
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    index = int(sys.argv[3])
except:
    print("You provided no area for closer inspection. Default plot will be created!")
    start = 0
    end = len(data_sound)

print("samples = {}".format(f))
print("Running script : ", sys.argv[0])
print("Number of arguments: ", len(sys.argv))
print("You chose those arguments: ", str(sys.argv))


# For direct testing purposes
# print(data_sound[0])
# print(data_mod_sound[0])
# print(abs((data_sound[0] - data_mod_sound[0]) / data_sound[0]))

# index is the wanted point where an average should be calculated
# width represents the range to the left and right of this given point
# both parameters are optional, but if you provide one you have to pass the other one as well.
def percentage_one(audio_org, audio_mod, index=None, width=None):
    rounds = len(audio_org)
    result = []

    if index is None:
        for i in range(rounds):
            if audio_org[i] == 0:
                value = 0.0
            elif audio_mod[i] == 0:
                value = 1
            else:
                value = abs(((audio_org[i] - audio_mod[i]) / audio_org[i]) * 100)
            result.append(value)

    # This part will trigger, when an optional index is provided for an average calculation based on the given parameter
    else:
        average_org = audio_org[index - width:index + width]
        average_mod = audio_mod[index - width:index + width]

        average_org_int = 0
        average_mod_int = 0

        for j in range(len(average_org)):
            average_org_int += average_org[j]
        average_org_int /= len(average_org)

        for k in range(len(average_mod)):
            average_mod_int += average_mod[k]
        average_mod_int /= len(average_mod)

        print("int")
        print(average_org_int)
        print("AVERAGE")
        print(average_org)

        for i in range(rounds):
            if audio_org[i] == 0:
                value = 0.0
            elif audio_mod[i] == 0:
                value = 1
            elif i == index:
                value = abs((average_mod_int - average_mod_int/average_org_int) * 100)
            else:
                value = abs(((audio_org[i] - audio_mod[i]) / audio_org[i]) * 100)
            result.append(value)
    return result[start:end]


def percentage_wav(audio_org, audio_mod):
    percentage = []

    rounds = len(audio_org)
    print(rounds)

    # getting the points
    org = audio_org
    mod = audio_mod

    # calculating the percentage
    for i in range(rounds):
        if org[i] == 0:
            value = 0.0  # cant calculate percentage increase from 0
        elif mod[i] == 0:
            value = 1  # if modified coefficient is 0, the change to coefficient is 100%
        else:
            # value = abs(100 - (mod_x[i] / org_y[i]) * 100)
            value = abs(1 - (mod[i] / org[i]))
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
            value = 0.0  # cant calculate percentage increase from 0
        elif mod[i] == 0:
            value = 1  # if modified coefficient is 0, the change to coefficient is 100%
        else:
            # value = abs(100 - (mod_x[i] / org_y[i]) * 100)
            value = abs((1 - mod[i] / org[i]))
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
    d = percentage_one(data_sound, data_mod_sound, 5, 5)  # .T[0]
    name = "44 Pianisten 01-Promenade"
    plt.title("Percentage of comparison of two signals")
    plt.ylabel("Percentage")
    plt.plot(d)

    plt.savefig(f'plot_images/percentage' + name)
    plt.show()
