import pywt
from os.path import dirname, join as pjoin
from scipy.io import wavfile
import scipy.io
from scipy.fftpack import fft
import matplotlib.pyplot as plt
import numpy as np
import random
import librosa as lro
import struct

audio_file_promenade_1 = "input_files/SaChenPromenade1.wav"


# https://stackoverflow.com/questions/16444726/binary-representation-of-float-in-python-bits-not-hex
def bin2float(b):
    ''' Convert binary string to a float.

    Attributes:
        :b: Binary string to transform.
    '''
    h = int(b, 2).to_bytes(8, byteorder="big")
    return struct.unpack('>d', h)[0]


def float2bin(f):
    ''' Convert float to 64-bit binary string.

    Attributes:
        :f: Float number to transform.
    '''
    [d] = struct.unpack(">Q", struct.pack(">d", f))
    return f'{d:064b}'


def process_audio_librosa():
    audio_file = "input_files/SaChenPromenade1.wav"
    signal_data, sample_rate = lro.load(audio_file, mono=False, sr=None)
    signal_size = len(signal_data)
    # sr=None keeps original sample rate, default value is 22050
    # signal_data = floating point numpy.ndarray where signal_data[t] corresponds
    # to the amplitude of the waveform at sample t. Dimensions of array = number of channels.
    # If you only want one channel, set mono=True. This converts the signal to mono (from e.g. stereo)
    print(f'Size of signal data: {signal_size}')
    print(signal_data)
    print(sample_rate)

    approx_coeffs, detail_coeffs = pywt.dwt(signal_data, 'db2')

    print(f'Approx coeffs: \n{approx_coeffs}')
    print(f'Detail coeffs: \n{detail_coeffs}')

    # choose message to be embedded as bitstring
    # only 1s
    msg = ""
    for i in range(len(detail_coeffs[0])):
        msg = msg + '1'


    # only use detail_coeffs of first channel to embed in this case:
    new_dc = detail_coeffs
    print(f'new_dc: {new_dc}')

    for i in range(len(detail_coeffs[0])):
        val = detail_coeffs[0][i]
        #print(f'old val: {val}')
        bin_val_list = list(float2bin(val))
        if msg[i] == '1':
            bin_val_list[-1] = '1'
        elif msg[i] == '0':
            bin_val_list[-1] = '0'

        new_bin_val = "".join(bin_val_list)
        #print(f'new val: {bin2float(new_bin_val)}')
        new_val = bin2float(new_bin_val)
        new_dc[0][i] = new_val

    print(f'new_dc after embedding: {new_dc}')
    reconstructed_signal = pywt.idwt(approx_coeffs, new_dc, 'db2')
    lro.output.write_wav("output_files/librosa_lsn_wtrmrkd.wav", np.asfortranarray(reconstructed_signal), sample_rate)


process_audio_librosa()


def read_audio_data2(file_path):
    sampling_frequency, audio_data = wavfile.read(file_path)
    return sampling_frequency, audio_data


def plot_dwt(time, approx_coeffs, detail_coeffs):
    plt.figure(1)
    plt.plot(time, approx_coeffs[:, 0], label="Approx. Coeffs")
    plt.plot(time, detail_coeffs[:, 1], label="Detail. Coeffs")
    plt.legend()
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.show()


def perform_dwt(sampling_frequency, audio_data, wavelet_type):
    print(audio_data)
    approx_coeffs, detail_coeffs = pywt.dwt(audio_data, wavelet_type)
    length = audio_data.shape[0] / sampling_frequency
    time = np.linspace(0., length, audio_data.shape[0])
    # plot_dwt(time, approx_coeffs, detail_coeffs)
    #print(detail_coeffs)
    return approx_coeffs, detail_coeffs, length


def generate_random_message(msg_length):
    random_int = random.randint(0, 2**msg_length-1)
    msg = '{0:b}'.format(random_int).zfill(msg_length)
    # print(msg)
    return msg


def embed_message(detail_coeffs):
    # coeffs: numpy.ndarray
    message = generate_random_message(len(detail_coeffs))
    new_detail_coeffs = detail_coeffs
    for i in range(0, len(detail_coeffs)-1):
        # print(detail_coeffs[i][0])
        new_detail_coeffs[i][0] = detail_coeffs[i][0] + int(message[i])
        new_detail_coeffs[i][1] = detail_coeffs[i][1] + int(message[i])
        new_detail_coeffs[i][2] = detail_coeffs[i][2] + int(message[i])

    return new_detail_coeffs


def reconstruct_audio(approx_coeffs, detail_coeffs, wavelet_type, sampling_freq):
    reconstructed_signal = pywt.idwt(approx_coeffs, detail_coeffs, wavelet_type)

    #for i in range(len(reconstructed_signal)):
    #    reconstructed_signal[i][0] = round(reconstructed_signal[i][0], 0)
    #    reconstructed_signal[i][1] = round(reconstructed_signal[i][1], 0)

    int_signal = reconstructed_signal.astype('int16')
    print(int_signal)

    print(reconstructed_signal)
    wavfile.write("watermarked_signal.wav", sampling_freq, reconstructed_signal.astype('int16'))


def do():
    wavelet_type = 'db3'
    sampling_freq, audio_data = read_audio_data2(audio_file_promenade_1)
    ac, dc, length = perform_dwt(sampling_freq, audio_data, wavelet_type)
    new_dc = embed_message(dc)
    reconstruct_audio(ac, new_dc, wavelet_type, sampling_freq)


# do()


def plot_wt():
    sampling_frequency, data = wavfile.read(audio_file_promenade_1)

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


def plot_fft(audio_file):
    rate, aud_data = wavfile.read(audio_file)

    len_data = len(aud_data)

    channel_1 = np.zeros(2 ** (int(np.ceil(np.log2(len_data)))))
    channel_1[0:len_data] = aud_data[:, 0]

    fourier = np.fft.fft(channel_1)

    # rate, aud_data = scipy.io.wavfile.read(file)
    ii = np.arange(0, len_data)
    t = ii / rate
    aud_data = np.zeros(len(t))
    for w in range(0, 15000, 250):
        aud_data += np.cos(2 * np.pi * w * t)

    # From here down, everything else can be the same
    len_data = len(aud_data)

    channel_1 = np.zeros(2 ** (int(np.ceil(np.log2(len_data)))))
    channel_1[0:len_data] = aud_data

    fourier = np.fft.fft(channel_1)
    w = np.linspace(0, 44000, len(fourier))

    # First half is the real component, second half is imaginary
    fourier_to_plot = fourier[0:len(fourier) // 2]
    w = w[0:len(fourier) // 2]

    plt.figure(1)

    plt.plot(w, fourier_to_plot)
    plt.xlabel('frequency')
    plt.ylabel('amplitude')
    plt.show()


def plot_fft_2(file):
    rate, data = wavfile.read(file)
    fft_out = fft(data)
    plt.plot(data, np.abs(fft_out))
    plt.show()


def test():
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
