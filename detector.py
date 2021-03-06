from audio_file import AudioFile
import pywt


class Detector:
    """
    Extract potential messages from sound file
    """

    def __init__(self, filepath: str, wavelet_type: str = "db2", embed_bit: int = 12):
        """
        Initialize detector object
        :param filepath: Path to input audio file.
        :param wavelet_type: Type of mother wavelet. Default = 'db2'.
        :param embed_bit: Position of bit in 32 bit floating point number where to detect message bits in coefficient.
        """
        self.audio_file = AudioFile(filepath)
        self.wavelet_type = wavelet_type
        self.embed_bit = embed_bit
        self.detail_coeffs = None
        self.approx_coeffs = None
        self.detected_message = None
        self.detect()

    def detect(self):
        """
        Extract message from bits at position embed_bit of each coefficient.
        """
        print(f'\nEXTRACTION USING MARKED FILE ---> WAVELET= {self.wavelet_type}, EMBED_BIT={self.embed_bit}'
              f'\n--------------------------')

        self.approx_coeffs, self.detail_coeffs = pywt.dwt(self.audio_file.signal_data, self.wavelet_type)

        extracted_message = ""
        for i in range(len(self.detail_coeffs[0])):
            val = self.detail_coeffs[0][i]
            bin_val_list = list(AudioFile.float2bin(val))
            extracted_message = extracted_message + str(bin_val_list[self.embed_bit])

        print(f'Extracted message:\n (First 64 bits): {extracted_message[:64]},'
              f' (last 64 bits): {extracted_message[-64:]}')
        self.detected_message = extracted_message

    def detect_blind(self):
        # TODO: implement blind detection without the need for embedding bit. Need some measure to check if detected
        #   message qualifies as a successful detection
        return True
