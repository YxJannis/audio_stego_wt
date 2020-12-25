import pywt
import soundfile


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
        # read file
        self.audio_data, self.sampling_rate = soundfile.read(self.file_path)
        self.size = self.audio_data.shape[0]
        self.length = self.size / self.sampling_rate

    def dwt(self, wavelet_type):
        # perform dwt on audio file
        self.approx_coeffs, self.detail_coeffs = pywt.dwt(self.audio_data, wavelet_type)
        return self.approx_coeffs, self.detail_coeffs
