import pywt
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
import argparse

audio_file_promenade_1 = "input_files/SaChenPromenade1.wav"

"""def plot_dwt(time, approx_coeffs, detail_coeffs):
    plt.figure(1)
    plt.plot(time, approx_coeffs[:, 0], label="Approx. Coeffs")
    plt.plot(time, detail_coeffs[:, 1], label="Detail. Coeffs")
    plt.legend()
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.show()"""


def plot_wt(audio_file, ax=None):
    sampling_frequency, data = wavfile.read(audio_file)

    print(f"number of channels = {data.shape[1]}")
    length = data.shape[0] / sampling_frequency
    print(f"length = {length}s")
    time = np.linspace(0., length, data.shape[0])

    plt.plot(time, data[:, 0], label="Left channel")
    plt.plot(time, data[:, 1], label="Right channel")
    plt.title("Stereo")
    plt.legend()

    return plt


def plot_coeff(audio_file, ax=None):
    sampling_frequency, data = wavfile.read(audio_file)

    # plt.figure()
    print(f"number of channels = {data.shape[1]}")
    length = data.shape[0] / sampling_frequency
    print(f"length = {length}s")
    time = np.linspace(0., length, data.shape[0])

    approx_coeffs, detail_coeffs = pywt.dwt(data, 'db3')

    plt.plot(time, approx_coeffs, label="Approx. Coeffs")
    plt.plot(time, detail_coeffs, label="Detail. Coeffs")
    plt.legend()
    plt.title("coeffs")

    return plt


def plot_diff(difference_array, ax=None):
    plt.plot(difference_array)
    plt.xticks([1, 500000, 1000000, len(difference_array)], [10, 500000, 1000000, len(difference_array)])
    return plt


def plot_master(audio_file, difference_array):
    parser = argparse.ArgumentParser(description='Enter the wanted plots.')
    parser.add_argument('-s', '--stereo', help='Request the stereo plot', default='check_string_for_empty',
                        required=False)
    parser.add_argument('-d', '--difference', help="Request the difference plot", default='check_string_for_empty_',
                        required=False)
    parser.add_argument('-c', '--coefficients', help="Request the coefficient plot", default='check_string_for_empty_c',
                        required=False)
    args = parser.parse_args()

    num = 0

    fig, (ax1, ax2, ax3) = plt.subplots(3)

    if args.stereo:
        num += 1
        fig.add_subplot(3, 1, num)
        print("Stereo plot creating...")
        plot_wt(audio_file, ax1)

    if args.difference:
        num += 1
        fig.add_subplot(3, 1, num)
        print("Difference plot creating...")
        plot_diff(difference_array, ax2)

    if args.coefficients:
        num += 1
        fig.add_subplot(3, 1, num)
        print("Coeffs plot creating...")
        plot_coeff(audio_file, ax3)

    plt.savefig('plot_images/plot.png')
    plt.show()


if __name__ == '__main__':
    # plot_wt(audio_file_promenade_1)
    a = [0.98, -0.98, 0.05, -0.05, 0.42, -0.42]
    # plot_diff(a)
    plot_master(audio_file_promenade_1, a)

    """em_bit = 20
    e = emb.Embedder("input_files/SaChenPromenade1.wav")
    length = e.cover_audio_file.signal_data[0]/e.cover_audio_file.sampling_rate
    time = np.linspace(0., length, e.cover_audio_file.signal_data.shape[0])
    plot_dwt(time , e.approx_coeffs, e.detail_coeffs)"""
