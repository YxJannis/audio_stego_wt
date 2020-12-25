import soundfile
import struct
import random


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

    def write_file(self, transpose: bool = True):
        """
        Write signal data, sampling rate to file path
        :param transpose: True if signal data needs to be transposed (e.g. using soundfile.read and write)
        """
        if transpose:
            soundfile.write(self.file_path, self.signal_data.T, self.sampling_rate, subtype='PCM_32')
        else:
            soundfile.write(self.file_path, self.signal_data, self.sampling_rate, subtype='PCM_32')

    # https://stackoverflow.com/questions/16444726/binary-representation-of-float-in-python-bits-not-hex
    @staticmethod
    def bin2float(b):
        """ Convert binary string to a float. """
        h = int(b, 2).to_bytes(8, byteorder="big")
        return struct.unpack('>d', h)[0]

    # https://stackoverflow.com/questions/16444726/binary-representation-of-float-in-python-bits-not-hex
    @staticmethod
    def float2bin(f):
        """ Convert float to 64-bit binary string."""
        [d] = struct.unpack(">Q", struct.pack(">d", f))
        return f'{d:064b}'

    @staticmethod
    def generate_random_message(message_length):
        """
        Generate random message as a bitstring.
        :param message_length: Length of random message.
        :return: Random bitstring.
        """
        random_int = random.randint(0, 2**message_length - 1)
        msg = '{0:b}'.format(random_int).zfill(message_length)
        return msg
