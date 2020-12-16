from scipy.io import wavfile
import pywt


class AudioFile:
    def __init__(self, file_path):
        self.file_path = file_path
        self.sampling_frequency = None
        self.audio_data = None
        self.length = None
        self.size = None
        self.approx_coeffs = None
        self.detail_coeffs = None
        self.read_file()

    def read_file(self):
        # read file with scipy.io wavfile
        self.sampling_frequency, self.audio_data = wavfile.read(self.file_path)
        self.size = self.audio_data.shape[0]
        self.length = self.size / self.sampling_frequency

    def dwt(self, wavelet_type):
        # perform dwt on audio file
        self.approx_coeffs, self.detail_coeffs = pywt.dwt(self.audio_data, wavelet_type)
        return self.approx_coeffs, self.detail_coeffs
