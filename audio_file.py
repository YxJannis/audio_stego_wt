import soundfile
import struct
import random


class AudioFile:
    """
    Manage audio files for embedding messages in wavelet (transform) domain
    """

    def __init__(self, file_path, sampling_rate: int = None, read: bool = True):
        """
        Initialize AudioFile object
        :param file_path: Path of audio file
        :param sampling_rate: Sampling rate of audio file (extracted automatically if paramter read not set manually)
        :param read: True: Read file automatically from filepath, False: don't read file from filepath
                     (e.g. for creating and writing files)
        """
        self.file_path = file_path
        self.write_file_subtype = None
        self.sampling_rate = sampling_rate
        self.signal_data = None
        self.max_message_len = None
        self.size = None
        self.approx_coeffs = None
        self.detail_coeffs = None

        if read:
            self.read_file()

    def read_file(self):
        """
        Read signal_data, sampling rate, signal size and maximum length of a potential watermark for wt embedding
        """
        self.signal_data, self.sampling_rate = soundfile.read(self.file_path)
        self.signal_data = self.signal_data.T
        self.size = self.signal_data.shape[0]
        self.max_message_len = self.size / self.sampling_rate

    def write_file(self, write_file_subtype: str = 'PCM_16', transpose: bool = False):
        """
        Write signal data, sampling rate to file path
        :param write_file_subtype: Subtype for output .wav file. Subtypes can impact the size of the output file.
        See https://pysoundfile.readthedocs.io/en/latest/#soundfile.available_subtypes for possible values.
        :param transpose: True if signal data needs to be transposed (e.g. using soundfile.read and write)
        """
        self.write_file_subtype = write_file_subtype
        if transpose:
            soundfile.write(self.file_path, self.signal_data.T, self.sampling_rate, subtype=write_file_subtype)
        else:
            soundfile.write(self.file_path, self.signal_data, self.sampling_rate, subtype=write_file_subtype)

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
        return f'{d:032b}'

    @staticmethod
    def generate_random_message(message_length: int, seed: int = 123):
        """
        Generate pseudorandom message as a bitstring.
        :param seed: seed for pseudorandom number
        :param message_length: Length of pseudorandom message.
        :return: Random bitstring.
        """
        random.seed(seed)
        random_int = random.randint(0, 2**message_length - 1)
        msg = '{0:b}'.format(random_int).zfill(message_length)
        return msg

    @staticmethod
    def check_error_rate(original_msg: str, detected_msg: str):
        """
        Compares two bit-strings and returns error rate of second string:
        Error rate = flipped bits in detected_msg compared to original_msg / len(detected_msg)
        :param original_msg: First bit-string.
        :param detected_msg: Second bit-string.
        :return: Error rate of second bit-string compared to first bit-string.
        """
        faults = 0
        for i in range(len(detected_msg)):
            if detected_msg[i] != original_msg[i]:
                faults = faults + 1
        return faults/len(detected_msg)

