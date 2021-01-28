from pywt import wavedec
from audio_file import AudioFile


class Decomposition:
    """
    Perform multilevel wavelet transform decomposition on audio files.
    """

    def __init__(self, audio_file: AudioFile):
        self.audio_file = audio_file
        self.signal_data = audio_file.signal_data.T

    # Keep in mind: Stereo audio has 2 channels therefore also two lists for each coeff (1 for each channel)
    def decomposition(self, level: int = 1, wavelet_type: str = 'db2', print_out: bool = False):
        """
        Multilevel decomposition using discrete wavelet transform.
        :param level: maximum depth of decomposition
        :param wavelet_type: wavelet used for discrete wavelet transform
        :param print_out: print overview of detail coefficients for each level on console
        :return: list of size level +1 containing approximation coefficients followed by
         detail coefficients of each level
        """
        data = wavedec(data=self.signal_data, wavelet=wavelet_type, level=level)
        if print_out:
            print(f'\n\n-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-'
                  f'+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+'
                  f'\nDecomposition for level {level}:\n\n')
            print(f'Approximation coefficients:\n {data[0][0]}\n\n')
            print(f'Detail coefficients:\n')
            for j in range(level):
                print(f'Level {level - j}:')
                print(f'Array size: {len(data[j + 1][0])}')
                print(f'{data[j + 1][0]}\n')
        return data


if __name__ == '__main__':
    cover_audio_file = AudioFile('input_files/SaChenPromenade1.wav')
    wavelet = 'db2'
    decomp = Decomposition(cover_audio_file)
    decomp.decomposition(wavelet_type=wavelet, level=5, print_out=True)
