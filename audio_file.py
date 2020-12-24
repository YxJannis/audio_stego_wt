from scipy.io import wavfile
import librosa as lro
import pywt


class AudioFile:
    def __init__(self, file_path):
        self.file_path = file_path
        self.sampling_rate = None
        self.audio_data = None
        self.length = None
        self.size = None
        self.approx_coeffs = None
        self.detail_coeffs = None
        self.read_file()

    def read_file(self):
        # read file using librosa
        self.audio_data, self.sampling_rate = lro.load(self.file_path, mono=False, sr=None)
        # sr=None keeps original sample rate, default value is 22050
        # signal_data = floating point numpy.ndarray where signal_data[t] corresponds
        # to the amplitude of the waveform at sample t. Dimensions of array = number of channels.
        # If you only want one channel, set mono=True. This converts the signal to mono (from e.g. stereo)
        self.size = self.audio_data.shape[0]
        self.length = self.size / self.sampling_rate

    def dwt(self, wavelet_type):
        # perform dwt on audio file
        self.approx_coeffs, self.detail_coeffs = pywt.dwt(self.audio_data, wavelet_type)
        return self.approx_coeffs, self.detail_coeffs
