from audio_file import AudioFile
import pywt
import soundfile


class Detector:
    def __init__(self, audio_file: AudioFile, embed_bit: int):
        self.audio_file = AudioFile
        self.embed_bit = embed_bit

    def detect(self):
        print(f'\n\nEXTRACTION USING MARKED FILE ---> EMBED_BIT={self.embed_bit}\n--------------------------')
        input_file_name = 'output_files/wt_bit' + str(self.embed_bit) + '_embedding.wav'
        marked_audio_file = input_file_name
        m_signal_data, m_sample_rate = soundfile.read(marked_audio_file)

        approx_coeffs, detail_coeffs = pywt.dwt(m_signal_data.T, 'db2')
        print(f'Detail_coefficients for channel 1: \n{detail_coeffs[0]}')

        extracted_message = ""
        for i in range(len(detail_coeffs[0])):
            val = detail_coeffs[0][i]
            bin_val_list = list(AudioFile.float2bin(val))
            extracted_message = extracted_message + str(bin_val_list[self.embed_bit])

        print(
            f'Extracted message:\n (First 64 bits): {extracted_message[:64]},'
            f' (last 64 bits): {extracted_message[-64:]}')

