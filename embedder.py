import random
import pywt
import librosa as lro
from scipy.io import wavfile
from audio_file import AudioFile
import struct


class Embedder:
    def __init__(self, audio_file: AudioFile, wavelet_type: str = "db2", msg: str = None, embed_bit: int = 10,
                 output_file_name: str = None):
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
            self.message = self.generate_random_message(self.max_message_length)
        else:
            if len(msg) > self.max_message_length:
                print("Message (in bits) can not be longer than " + str(self.max_message_length) +
                      ". Generating file with random message using maximal length.")
                self.message = self.generate_random_message(self.max_message_length)
            else:
                self.message = msg.zfill(self.max_message_length)

        self.approx_coeffs = None
        self.detail_coeffs = None
        self.marked_detail_coeffs = None
        self.embed()
        self.reconstruct_audio()

    # https://stackoverflow.com/questions/16444726/binary-representation-of-float-in-python-bits-not-hex
    @staticmethod
    def bin2float(b):
        """ Convert binary string to a float. """
        h = int(b, 2).to_bytes(8, byteorder="big")
        return struct.unpack('>d', h)[0]

    # https://stackoverflow.com/questions/16444726/binary-representation-of-float-in-python-bits-not-hex
    @staticmethod
    def float2bin(f):
        """ Convert float to 32-bit binary string."""
        [d] = struct.unpack(">Q", struct.pack(">d", f))
        return f'{d:032b}'

    @staticmethod
    def generate_random_message(message_length):
        # generate integer of size 'message_length'
        random_int = random.randint(0, 2**message_length - 1)
        # convert integer to bitstring
        msg = '{0:b}'.format(random_int).zfill(message_length)
        return msg

    def embed(self):
        print(f'EMBEDDING USING UNMODIFIED COVER FILE ---> EMBED_BIT={self.embed_bit}\n--------------------------')
        # dwt on audio_file
        self.approx_coeffs, self.detail_coeffs = self.audio_file.dwt(self.wavelet_type)
        self.marked_detail_coeffs = self.detail_coeffs
        print(f'Detail coefficients for channel 1: \n{self.detail_coeffs[0]}')
        print(f'Embedded message:\n (First 64 bits): {self.message[:64]}, (last 64 bits): {self.message[-64:]}')

        # only use detail_coeffs of first channel to embed in this case (detail_coeffs[0]).
        # convert float coefficient into binary representation and flip last bit to 1 or 0 according to the message
        for i in range(len(self.detail_coeffs[0])):
            val = self.detail_coeffs[0][i]
            bin_val_list = list(self.float2bin(val))
            if self.message[i] == '1':
                bin_val_list[self.embed_bit] = '1'
            elif self.message[i] == '0':
                bin_val_list[self.embed_bit] = '0'

            new_bin_val = "".join(bin_val_list)
            new_val = self.bin2float(new_bin_val)
            self.marked_detail_coeffs[0][i] = new_val
        print(f'Detail coefficients of channel 1 after embedding: \n{self.marked_detail_coeffs[0]}\n')
        # reconstruct signal with embedded watermark
        reconstructed_signal = pywt.idwt(self.approx_coeffs, self.marked_detail_coeffs, 'db2')
        output_file_name = 'output_files/wt_bit' + str(self.embed_bit) + '_embedding.wav'
        # TODO: soundfile.write
        # lro.output.write_wav(output_file_name, np.asfortranarray(reconstructed_signal), self.audio_file.sampling_rate)

    def reconstruct_audio(self):
        # TODO: is this function necessary?
        return 0


if __name__ == '__main__':
    sa_chen_promenade = AudioFile('SaChenPromenade1.wav')
    Embedder(sa_chen_promenade)
