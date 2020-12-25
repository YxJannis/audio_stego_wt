import pywt
import soundfile


class AudioFile:
    """
    Manage audio files for embedding messages in wavelet (transform) domain
    """

    def __init__(self, file_path):
        """
        Initialize AudioFile object
        :param file_path: path of audio file
        """
        self.file_path = file_path
        self.sampling_rate = None
        self.signal_data = None
        self.max_message_len = None
        self.size = None
        self.approx_coeffs = None
        self.detail_coeffs = None
        self.read_file()

    def read_file(self):
        """
        Read signal_data, sampling rate, signal size and maximum length of a potential watermark for wt embedding
        """
        self.signal_data, self.sampling_rate = soundfile.read(self.file_path)
        self.size = self.signal_data.shape[0]
        self.max_message_len = self.size / self.sampling_rate
