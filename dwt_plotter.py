import pywt
from scipy.io import wavfile
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from embedder import Embedder
from detector import Detector
import percentage

audio_file_promenade_1 = "input_files/SaChenPromenade1.wav"


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


def plot_master(emb: Embedder, det: Detector, file_title: str, message_seed: int = None):
    mpl.rcParams['agg.path.chunksize'] = 10000
    og_signal_data = emb.cover_audio_file.signal_data[0]          # [0] for channel 1
    emb_signal_data = emb.reconstructed_audio.signal_data[0]        # [0] for channel 1
    det_signal_data = det.audio_file.signal_data[0]

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


def plot_error_dist_rates(error_rates: list, double_error_rates: list, triple_error_rates: list, embed_bits: list,
                          name: str = 'default'):
    x_vals = embed_bits
    plt.xlabel('Embed Bit')

    max_value = 0.3

    for i in range(len(error_rates)):
        if error_rates[i] > max_value:
            error_rates[i] = max_value
    for i in range(len(double_error_rates)):
        if error_rates[i] > max_value:
            error_rates[i] = max_value
    for i in range(len(triple_error_rates)):
        if error_rates[i] > max_value:
            error_rates[i] = max_value
    ticks = [i/10 for i in range(0, int(max_value*10)+1)]
    plt.yticks(ticks, [f'{i}' for i in ticks[:-1]] + [f'>{ticks[-1]}'])
    plt.ylim(0, max_value)
    plt.xticks(embed_bits)
    plt.scatter(y=error_rates, x=x_vals, color='red', label='Single Error')
    plt.scatter(y=double_error_rates, x=x_vals, color='blue', label='Double Error')
    plt.scatter(y=triple_error_rates, x=x_vals, color='green', label='Triple Error')
    plt.ylabel("Error Rate")
    plt.legend(loc='upper center')
    plt.margins(y=0.1)
    # plt.show()
    plt.grid(axis='y', linestyle='--')
    plt.savefig(f'plot_images/{name}_rel.png')
    plt.close()


