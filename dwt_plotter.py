import pywt
from scipy.io import wavfile
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from embedder import Embedder
from detector import Detector
import argparse
import percentage

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


def plot_master_2(emb: Embedder, det: Detector, file_title: str, message_seed: int = None):
    mpl.rcParams['agg.path.chunksize'] = 10000
    og_signal_data = emb.cover_audio_file.signal_data.T[0]          # [0] for channel 1
    emb_signal_data = emb.reconstructed_audio.signal_data[0]        # [0] for channel 1
    det_signal_data = det.audio_file.signal_data.T[0]

    wavelet_type = emb.wavelet_type
    embed_bit = emb.embed_bit
    sampling_freq = emb.cover_audio_file.sampling_rate

    og_detail_coeffs = emb.detail_coeffs[0]
    emb_detail_coeffs = emb.marked_detail_coeffs[0]
    det_detail_coeffs = det.detail_coeffs[0]

    diff_sig_og_emb = og_signal_data - det_signal_data
    diff_percentage = percentage.percentage_wav_2(og_signal_data, det_signal_data)

    fig, axs = plt.subplots(2, 2, figsize=(15, 5))
    fig.suptitle(f'Wavelet: {wavelet_type}, Embed Bit: {embed_bit}, Seed: {message_seed}')

    # plot original audio data
    axs[0][0].plot(og_signal_data)
    axs[0][0].set_title('Audio data (unmodified)')

    # plot signal data from embedded file
    axs[1][0].plot(det_signal_data, 'tab:orange')
    axs[1][0].set_title('Audio data (modified)')
    axs[1][0].set_ylim(min(og_signal_data), max(og_signal_data))

    # plot differences
    axs[0][1].plot(diff_sig_og_emb, 'tab:red')
    axs[0][1].set_title('Signal diff. original vs. modified')
    axs[0][1].set_ylim(min(og_signal_data), max(og_signal_data))

    # plot percentage differences
    axs[1][1].plot(diff_percentage)
    axs[1][1].set_title('Signal diff. (percentage)')
    axs[1][1].set_ylim(0, 500)
    axs[1][1].set_yticks([0, 100, 200, 300, 400, 500])                      # upper bound percentage values by 500 and
    axs[1][1].set_yticklabels(['0', '100', '200', '300', '400', '> 500'])   # update y tick labels accordingly

    plt.subplots_adjust(hspace=0.4, wspace=0.3)
    plt.savefig(f'plot_images/{file_title}_{wavelet_type}_{embed_bit}.png')
    # plt.show()
    plt.close()


def plot_error_rates(values: dict, name: str = 'default'):
    lists = sorted(values.items())
    x, y = zip(*lists)
    plt.scatter(x, y)
    plt.xticks(range(min(x), max(x) + 1, 1))
    plt.yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    plt.title(name)
    plt.ylabel('Error Rate')
    plt.xlabel('Embed Bit')
    # plt.show()
    plt.savefig(f'plot_images/{name}.png')
    plt.close()


def plot_error_dist(error_rates: list, double_errors: list, triple_errors: list, embed_bits: list,
                    name: str = 'default'):
    fig, ax = plt.subplots()
    ax.scatter(y=error_rates, x=embed_bits, color='black', label='Error Rate', marker='o')
    ax.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    ax.set_xticks(embed_bits)
    ax.set_xlabel('Embed Bit')
    ax.set_ylabel('Error Rate')
    ax2 = ax.twinx()
    ax2.scatter(y=triple_errors, x=embed_bits, color='red', label='#Triple Errors', marker='o')
    ax2.scatter(y=double_errors, x=embed_bits, color='blue', label='#Double Errors', marker='o')
    ax2.set_ylabel("# of subsequent Errors", color='blue')
    plt.title(name)
    ax_lines, ax_labels = ax.get_legend_handles_labels()
    ax2_lines, ax2_labels = ax2.get_legend_handles_labels()
    ax2.set_yscale('log')
    plt.legend(ax_lines + ax2_lines, ax_labels + ax2_labels, loc='upper center')
    plt.grid(linestyle='--')
    # plt.show()
    plt.savefig(f'plot_images/{name}.png')
    plt.close()


def plot_error_dist_rates(error_rates: list, double_error_rates: list, triple_error_rates: list, embed_bits: list,
                          name: str = 'default'):
    x_vals = embed_bits
    fig, ax = plt.subplots()
    ax.set_xlabel('Embed Bit')
    ax.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7])
    ax.scatter(y=error_rates, x=x_vals, color='red', label='Single Error')
    ax.scatter(y=double_error_rates, x=x_vals, color='blue', label='Double Error')
    ax.scatter(y=triple_error_rates, x=x_vals, color='green', label='Triple Error')
    ax.set_ylabel("#Subsequent errors")
    plt.legend(loc='upper left')
    plt.show()
    plt.close()

