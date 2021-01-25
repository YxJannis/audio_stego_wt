import pywt
from audio_file import AudioFile

cover_audio_file = AudioFile('input_files/SaChenPromenade1.wav')
wavelet_type = 'db2'


# Keep in mind: Stereo audio has 2 channels therefore also two lists for each coeff (1 for each channel)
def multilevel_decomposition(level):
    data = pywt.wavedec(cover_audio_file.signal_data.T, wavelet=wavelet_type, level=level)
    return data


def print_coeffs(level):
    data = multilevel_decomposition(level)
    print(f'\n\n-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+'
          f'\nDecomposition for level {level}:\n\n')
    print(f'Approximation coefficients:\n {data[0][0]}\n\n')
    print(f'Detail coefficients:\n')
    for j in range(level):
        print(f'Level {level-j}:')
        print(f'Array size: {len(data[j + 1][0])}')
        print(f'{data[j + 1][0]}\n')


print_coeffs(6)

