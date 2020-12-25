from audio_file import AudioFile
import pywt


class Detector:
    """
    Extract potential messages from sound file
    """

    def __init__(self, audio_file: AudioFile, wavelet_type: str = "db2", embed_bit: int = 10):
        """
        Initialize detector object
        :param audio_file: path to input audio file
        :param wavelet_type: Type of mother wavelet. Default = 'db2'.
        :param embed_bit: Position of bit in 32 bit floating point number where to detect message bits in coefficient.
        """
        self.audio_file = audio_file
        self.wavelet_type = wavelet_type
        self.embed_bit = embed_bit
        self.detect()

    def detect(self):
        """
        Extract message from bits at position embed_bit of each coefficient
        :return: Extracted message
        """
        print(f'\n\nEXTRACTION USING MARKED FILE ---> EMBED_BIT={self.embed_bit}\n--------------------------')

        approx_coeffs, detail_coeffs = pywt.dwt(self.audio_file.signal_data.T, 'db2')
        print(f'Detail_coefficients for channel 1: \n{detail_coeffs[0]}')

        extracted_message = ""
        for i in range(len(detail_coeffs[0])):
            val = detail_coeffs[0][i]
            bin_val_list = list(AudioFile.float2bin(val))
            extracted_message = extracted_message + str(bin_val_list[self.embed_bit])

        print(f'Extracted message:\n (First 64 bits): {extracted_message[:64]},'
              f' (last 64 bits): {extracted_message[-64:]}')
        return extracted_message
