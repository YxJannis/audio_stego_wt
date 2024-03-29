import sys

import matplotlib.pyplot as plt
import soundfile as sf


# This function is used to gather all the needed information for the calculation process
def get_args(path_org, path_mod):
    data_sound, f = sf.read(path_org)
    data_mod_sound, f = sf.read(path_mod)

    try:
        start = int(sys.argv[1])
        end = int(sys.argv[2])

    except:
        print("You provided no area for closer inspection. Default plot will be created!")
        start = 0
        end = len(data_sound)

    try:
        index = int(sys.argv[3])
        width = int(sys.argv[4])
    except:
        index = None
        width = None
        print("No index and frame provided")

    print("samples = {}".format(f))
    print("Running script : ", sys.argv[0])
    print("Number of arguments: ", len(sys.argv))
    print("You chose those arguments: ", str(sys.argv))

    return data_sound, data_mod_sound, start, end, index, width


# index is the wanted point where an average should be calculated
# width represents the range to the left and right of this given point
# both parameters are optional, but if you provide one you have to pass the other one as well.
def percentage_one(audio_org, audio_mod, start=None, end=None, index=None, width=None):
    rounds = len(audio_org)
    result = []

    if index is None:
        print("First")
        for i in range(rounds):
            if audio_org[i] == 0:
                test = audio_org[i - 5: i + 5]
                for j in range(len(test)):
                    value += test[j]
                value /= len(test)
                # value = 0.0
            elif audio_mod[i] == 0:
                test = audio_mod[i - 5: i + 5]
                for j in range(len(test)):
                    value += test[j]
                value /= len(test)
                # value = 1
            else:
                value = abs(((audio_org[i] - audio_mod[i]) / audio_org[i]) * 100)
            result.append(value)

    # This part will trigger, when an optional index is provided for an average calculation based on the given parameter
    else:
        print("Second")

        average_org = audio_org[index - width: index + width]
        average_mod = audio_mod[index - width: index + width]

        average_org_int = 0
        average_mod_int = 0

        print(average_org)
        for j in range(len(average_org)):
            average_org_int += average_org[j]
        average_org_int /= len(average_org)

        for k in range(len(average_mod)):
            average_mod_int += average_mod[k]
        average_mod_int /= len(average_mod)

        print("int")
        print(average_org_int)
        print(average_mod_int)
        print("AVERAGE")
        print(average_org)

        for i in range(rounds):
            if audio_org[i] == 0:
                value = 0.0
            elif audio_mod[i] == 0:
                value = 1
            elif i == index:
                value = abs(1 - (average_org_int - average_mod_int / average_org_int))
                # value = abs((average_org_int - average_mod_int / average_org_int) * 100)
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


if __name__ == '__main__':
    path_org = "input_files/orig/44 Pianisten 01-Promenade.wav"
    path_mod = "output_files/mod/44 Pianisten 01-Promenade.wav"
    data_sound, data_mod_sound, start, end, index, width = get_args(path_org, path_mod)
    d = percentage_one(data_sound, data_mod_sound, start, end, index, width)  # .T[0]
    name = "44 Pianisten 01-Promenade"
    plt.title("Percentage of comparison of two signals")
    plt.ylabel("Percentage")
    plt.plot(d)

    plt.savefig(f'plot_images/percentage' + name)
    plt.show()
