import pywt
from audio_file import AudioFile
from detector import Detector


class Embedder:
    """
    Embed messages in wavelet (transform) domain.
    """

    def __init__(self, filepath: str, wavelet_type: str = "db2", msg: str = None, embed_bit: int = 10,
                 output_file_name: str = None, write_file_subtype: str = "PCM_16"):
        """
        Initialize Embedder.
        :param filepath: Path to audio file.
        :param wavelet_type: Type of mother wavelet. Default = 'db2'.
        :param msg: Message as bitstring. If shorter than embedding capacity, gets concatenated with 0s.
                    Default = randomly generated bitstring.
        :param embed_bit: Position of bit in 32 bit floating point number where to embed message bits in coefficient.
        :param output_file_name: File name of embedded file.
        """
        self.wavelet_type = wavelet_type
        self.cover_audio_file = AudioFile(filepath)
        self.embed_bit = embed_bit
        self.max_message_length = int(self.cover_audio_file.size / 2)
        self.write_file_subtype = write_file_subtype

        if output_file_name is None:
            self.output_file_name = 'output_files/wt_bit' + str(self.embed_bit) + '_embedding.wav'
        else:
            self.output_file_name = output_file_name

        # message size handling
        if msg is None:
            self.message = AudioFile.generate_random_message(self.max_message_length+1)
        else:
            if len(msg) > self.max_message_length+1:
                print(f'Message too long, will be cut off eventually.')
                self.message = msg
                #print(f'Message (in bits) can not be longer than {self.max_message_length+1}. '
                #      f'Generating file with random message using maximal length.')
                #self.message = AudioFile.generate_random_message(self.max_message_length+1)
            else:
                print(f'Message too short, will be filled with 0s to lenght {self.max_message_length+1}.')
                self.message = msg.zfill(self.max_message_length+1)

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
        self.approx_coeffs, self.detail_coeffs = pywt.dwt(self.cover_audio_file.signal_data.T, self.wavelet_type)
        self.marked_detail_coeffs = self.detail_coeffs.copy()
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

    def multilevel_decomposition(self):
        data = pywt.wavedec(self.cover_audio_file.signal_data.T, wavelet=self.wavelet_type, level=2)

    def reconstruct_and_write(self):
        """
        Reconstruct audio signal using inverse discrete wavelet transform and write to .wav file.
        :return: Reconstructed AudioFile with message embedded
        """
        reconstructed_audio = AudioFile(self.output_file_name, sampling_rate=self.cover_audio_file.sampling_rate,
                                        read=False)
        reconstructed_audio.signal_data = pywt.idwt(self.approx_coeffs, self.marked_detail_coeffs, self.wavelet_type)
        reconstructed_audio.write_file(transpose=True, write_file_subtype=self.write_file_subtype)
        return reconstructed_audio


if __name__ == '__main__':
    em_bit = 12
    e = Embedder(f'input_files/SaChenPromenade1.wav', output_file_name=f'output_files/wt_bit{em_bit}_embedding.wav',
                 embed_bit=em_bit)
    d = Detector(f'output_files/wt_bit{em_bit}_embedding.wav', embed_bit=em_bit)
    print(f'Error Rate: {AudioFile.check_error_rate(e.message, d.detected_message)}')


