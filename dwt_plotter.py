import pywt
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np


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

    fig1, ax1 = plt.subplots()

    time = np.linspace(0., length, data.shape[0])
    ax1.plot(time, data[:, 0], label="Left channel")
    ax1.plot(time, data[:, 1], label="Right channel")
    ax1.legend()
    ax1.set_xlabel("Time [s]")
    ax1.set_ylabel("Amplitude")

    #
    scales = (1, len(data))
    approx_coeffs, detail_coeffs = pywt.dwt(data, 'db3')

    print(approx_coeffs)
    print(detail_coeffs)

    plt.figure(2)
    plt.plot(time, approx_coeffs, label="Approx. Coeffs")
    plt.plot(time, detail_coeffs, label="Detail. Coeffs")
    plt.legend()
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.show()


def test():  # TODO Chunk, skipped.
    wav_fname = 'input_files/file_example_WAV_2MG.wav'

    samplerate, data = wavfile.read(wav_fname)
    wavfile.write("testout.wav", samplerate, data.astype('int16'))
    print(f"number of channels = {data.shape[1]}")

    length = data.shape[0] / samplerate
    print(f"length = {length}s")

    time = np.linspace(0., length, data.shape[0])
    plt.plot(time, data[:, 0], label="Left channel")
    plt.plot(time, data[:, 1], label="Right channel")
    plt.legend()
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.show()


if __name__ == '__main__':
    plot_wt(audio_file_promenade_1)

    """em_bit = 20
    e = emb.Embedder("input_files/SaChenPromenade1.wav")
    length = e.cover_audio_file.signal_data[0]/e.cover_audio_file.sampling_rate
    time = np.linspace(0., length, e.cover_audio_file.signal_data.shape[0])
    plot_dwt(time , e.approx_coeffs, e.detail_coeffs)"""