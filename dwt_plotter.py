import pywt
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
import argparse

audio_file_promenade_1 = "input_files/SaChenPromenade1.wav"


def plot_dwt(time, approx_coeffs, detail_coeffs):
    plt.figure(1)
    plt.plot(time, approx_coeffs[:, 0], label="Approx. Coeffs")
    plt.plot(time, detail_coeffs[:, 1], label="Detail. Coeffs")
    plt.legend()
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.show()


def plot_wt(audio_file):
    sampling_frequency, data = wavfile.read(audio_file)

    print(f"number of channels = {data.shape[1]}")
    length = data.shape[0] / sampling_frequency
    print(f"length = {length}s")
    time = np.linspace(0., length, data.shape[0])

    plt.figure()
    plt.subplot(2, 1, 1)

    plt.plot(time, data[:, 0], label="Left channel")
    plt.plot(time, data[:, 1], label="Right channel")
    plt.title("Stereo")
    plt.legend()

    approx_coeffs, detail_coeffs = pywt.dwt(data, 'db3')

    plt.subplot(2, 1, 2)
    plt.plot(time, approx_coeffs, label="Approx. Coeffs")
    plt.plot(time, detail_coeffs, label="Detail. Coeffs")
    plt.legend()
    plt.title("coeffs")

    return plt
    # plt.show()


def plot_diff(difference_array):
    plt.figure()
    plt.plot(difference_array)
    plt.xticks([1, 500000, 1000000, len(difference_array)], [10, 500000, 1000000, len(difference_array)])
    return plt
    # plt.show()


def plot_master(audio_file, difference_array):
    parser = argparse.ArgumentParser(description='Enter the wanted plots.')
    parser.add_argument('-s', '--stereo', help='Request the stereo plot', default='check_string_for_empty', required=False)
    parser.add_argument('-d', '--difference', help="Request the difference plot", default='check_string_for_empty_', required=False)
    args = parser.parse_args()

    if args.stereo:
        print("Stereo plot creating...")
        ax = plot_wt(audio_file)
        ax.savefig('plot_images/stereo_plot.png')
        ax.show()

    if args.difference:
        print("Difference plot creating...")
        ay = plot_diff(difference_array)
        ay.savefig('plot_images/difference_plot.png')
        ay.show()


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
