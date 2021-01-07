import pywt
from scipy.io import wavfile
from scipy.fftpack import fft
import matplotlib.pyplot as plt
import numpy as np
import random
import librosa as lro
import soundfile
import struct


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


def test(): #TODO Chunk, skipped.
    wav_fname = 'input_files/file_example_WAV_2MG.wav'

    samplerate, data = wavfile.read(wav_fname)
    wavfile.write("testout.wav", samplerate, data.astype('int16'))
    print(f"number of channels = {data.shape[1]}")

    length = data.shape[0] / samplerate
    print(f"length = {length}s")

    import matplotlib.pyplot as plt
    import numpy as np
    time = np.linspace(0., length, data.shape[0])
    plt.plot(time, data[:, 0], label="Left channel")
    plt.plot(time, data[:, 1], label="Right channel")
    plt.legend()
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.show()
