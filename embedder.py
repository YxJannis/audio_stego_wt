import random
import pywt
from audio_file import AudioFile
import struct
import soundfile


class Embedder:
    """
    Embed messages in wavelet (transform) domain.
    """

    def __init__(self, audio_file: AudioFile, wavelet_type: str = "db2", msg: str = None, embed_bit: int = 10,
                 output_file_name: str = None):
        """
        Initialize Embedder.
        :param audio_file: Valid :py:class: `audio_file` object.
        :param wavelet_type: Optional wavelet type. Default = 'db2'.
        :param msg: Optional message as bitstring. Default = randomly generated bitstring.
        :param embed_bit: Position of bit in 32 bit floating point number where to embed message bits in coefficient.
        :param output_file_name: File name of embedded file.
        """
        self.wavelet_type = wavelet_type
        self.audio_file = audio_file
        self.embed_bit = embed_bit
        self.max_message_length = int(self.audio_file.size/2)

        if output_file_name is None:
            self.output_file_name = 'output_files/wt_bit' + str(self.embed_bit) + '_embedding.wav'
        else:
            self.output_file_name = output_file_name

        # message size handling
        if msg is None:
            self.message = AudioFile.generate_random_message(self.max_message_length)
        else:
            if len(msg) > self.max_message_length:
                print("Message (in bits) can not be longer than " + str(self.max_message_length) +
                      ". Generating file with random message using maximal length.")
                self.message = AudioFile.generate_random_message(self.max_message_length)
            else:
                self.message = msg.zfill(self.max_message_length)

        self.approx_coeffs = None
        self.detail_coeffs = None
        self.marked_detail_coeffs = None
        self.embed()
        self.reconstruct_and_write()

    def embed(self):
        """
        Embed message in signal data using discrete wavelet transform.
        * signal_data: raw data of AudioFile object given in init
        * embed_bit: position of message-bit substitution in detail coefficients
        * wavelet_type: type of mother wavelet for discrete wavelet transform. Defined in init, default 'db2'
        * message: message to be embedded. Defined in init (or generated randomly)
        """
        print(f'EMBEDDING USING UNMODIFIED COVER FILE ---> EMBED_BIT={self.embed_bit}\n--------------------------')
        # dwt on audio_file, transpose signal data due to soundfile.read array shape
        self.approx_coeffs, self.detail_coeffs = pywt.dwt(self.audio_file.signal_data.T, self.wavelet_type)
        self.marked_detail_coeffs = self.detail_coeffs
        print(f'Detail coefficients for channel 1: \n{self.detail_coeffs[0]}')
        print(f'Embedded message:\n (First 64 bits): {self.message[:64]}, (last 64 bits): {self.message[-64:]}')

        # only use detail_coeffs of first channel to embed in this case (detail_coeffs[0]).
        # convert float coefficient into binary representation and flip last bit to 1 or 0 according to the message
        for i in range(len(self.detail_coeffs[0])):
            val = self.detail_coeffs[0][i]
            bin_val_list = list(AudioFile.float2bin(val))
            if self.message[i] == '1':
                bin_val_list[self.embed_bit] = '1'
            elif self.message[i] == '0':
                bin_val_list[self.embed_bit] = '0'

            new_bin_val = "".join(bin_val_list)
            new_val = AudioFile.bin2float(new_bin_val)
            self.marked_detail_coeffs[0][i] = new_val
        print(f'Detail coefficients of channel 1 after embedding: \n{self.marked_detail_coeffs[0]}\n')

    def reconstruct_and_write(self):
        """
        Reconstruct audio signal using inverse discrete wavelet transform and write to .wav file.
        """
        reconstructed_signal = pywt.idwt(self.approx_coeffs, self.marked_detail_coeffs, self.wavelet_type)
        soundfile.write(self.output_file_name, reconstructed_signal.T, self.audio_file.sampling_rate, subtype='PCM_32')


if __name__ == '__main__':
    sa_chen_promenade = AudioFile('SaChenPromenade1.wav')
    Embedder(sa_chen_promenade)
