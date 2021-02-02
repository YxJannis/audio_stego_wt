import pywt
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
from embedder import Embedder
from detector import Detector
import argparse

audio_file_promenade_1 = "input_files/SaChenPromenade1.wav"


def plot_wt(audio_file, ax=None):
    sampling_frequency, data = wavfile.read(audio_file)

    print(f"number of channels = {data.shape[1]}")
    length = data.shape[0] / sampling_frequency
    print(f"length = {length}s")
    time = np.linspace(0., length, data.shape[0])

    plt.plot(time, data.T[0], label="Left channel")
    plt.title("Audio Data (left channel)")

    return plt


def plot_coeff(audio_file, ax=None):
    sampling_frequency, data = wavfile.read(audio_file)

    # plt.figure()
    print(f"number of channels = {data.shape[1]}")
    length = data.shape[0] / sampling_frequency
    print(f"length = {length}s")
    time = np.linspace(0., length, data.shape[0])

    approx_coeffs, detail_coeffs = pywt.dwt(data, 'db2')

    # plt.plot(time, approx_coeffs, label="Approx. Coeffs")
    plt.plot(time, detail_coeffs.T[0], label="Detail. Coeffs")
    # plt.legend()
    plt.title("Detail coefficients (left channel)")

    return plt


def plot_diff(difference_array, ax=None):
    plt.title("Difference (original vs. embedded)")
    plt.plot(difference_array)
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

    fig, [ax1, ax2, ax3] = plt.subplots(3)

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

    fig.tight_layout()
    plt.savefig('plot_images/plot.png')
    plt.show()


def plot_master_2(emb: Embedder, det: Detector, file_title: str):
    og_signal_data = emb.cover_audio_file.signal_data.T[0]  # [0] for channel 1
    emb_signal_data = emb.reconstructed_audio.signal_data[0]

    wavelet_type = emb.wavelet_type
    embed_bit = emb.embed_bit
    sampling_freq = emb.cover_audio_file.sampling_rate

    og_detail_coeffs = emb.detail_coeffs[0]
    emb_detail_coeffs = emb.marked_detail_coeffs[0]
    det_detail_coeffs = det.detail_coeffs[0]

    fig, axs = plt.subplots(2, 2)
    fig.suptitle(f'Wavelet: {wavelet_type}, Embed Bit: {embed_bit}')

    # plot original audio data
    axs[0][0].plot(og_signal_data)
    axs[0][0].set_title('Audio data (unmodified)')
    #axs[0][0].set_ylim(min(og_signal_data), max(og_signal_data))

    axs[1][0].plot(emb_signal_data, 'tab:orange')
    axs[1][0].set_title('Audio data (modified)')
    #axs[1][0].set_ylim(y_lim)
    #axs[1][0].set_ylim(min(og_signal_data), max(og_signal_data))
    #axs[1][0].set_xlim(signal_data_x_lim)

    # plot detail coeffs
    # TODO: remove detail coeffs? and replace with percentage change of differences?
    axs[0][1].scatter(og_detail_coeffs)
    axs[0][1].set_title('Detail coefficients (unmodified)')
    #axs[0][1].set_ylim(y_lim)
    #axs[0][1].set_ylim(min(og_signal_data), max(og_signal_data))

    # plot differences
    diff_sig_og_emb = og_signal_data - emb_signal_data
    axs[1][1].plot(diff_sig_og_emb, 'tab:red')
    axs[1][1].set_title('Signal diff. original vs. modified')
    #axs[1][1].set_ylim(y_lim)
    #axs[1][1].set_ylim(min(og_signal_data), max(og_signal_data))
    #axs[1][1].set_xlim(signal_data_x_lim)

    plt.subplots_adjust(hspace=0.4, wspace=0.3)
    # plt.tight_layout()
    plt.savefig(f'plot_images/{file_title}_{wavelet_type}_{embed_bit}.png')
    # plt.show()
    plt.close()


def plot_values(values: dict, name: str = 'default'):
    lists = sorted(values.items())
    x, y = zip(*lists)
    plt.scatter(x, y)
    plt.xticks(range(min(x), max(x) + 1, 1))
    plt.yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    plt.title(name)
    plt.ylabel('Error Rate')
    plt.xlabel('Embed Bit')
    # plt.show()
    plt.savefig(f'plot_images/{name}')
    plt.close()

# if __name__ == '__main__':
# plot_wt(audio_file_promenade_1)
# a = [0.98, -0.98, 0.05, -0.05, 0.42, -0.42]
# plot_diff(a)
# plot_master(audio_file_promenade_1, a)
