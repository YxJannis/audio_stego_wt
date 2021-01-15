import pywt
from audio_file import AudioFile

cover_audio_file = AudioFile('input_files/SaChenPromenade1.wav')
wavelet_type = 'db2'


# Keep in mind: Stereo audio has 2 channels therefore also two lists for each coeff (1 for each channel)
def multilevel_decomposition(level):
    data = pywt.wavedec(cover_audio_file.signal_data.T, wavelet=wavelet_type, level=level)
    return data


def check_levels():
    for i in range(1, 6):
        data = multilevel_decomposition(i)
        print(f'\n\n-+-+-+-+-+-+-+-+-+-+-+-+-+\nDecomposition for level {i}:\n\n')
        print(f'Coefficients (for channel 1) array size: {len(data[0][0])}')
        print(f'Detail coeffs at level 1: {data[1][0]}')
        try:
            print(f'Detail coeffs at level 2: {data[2][0]}')
            print(f'Detail coeffs at level 3: {data[3][0]}')
        except:
            True


def print_coeffs():
    data = multilevel_decomposition(3)
    print(f'{data}')
    print(f'\n-----------\n{data[0][0]}')
    print(f'\n-----------\n{data[1][0]}')
    print(f'\n-----------\n{data[2][0]}')
    print(f'\n-----------\n{data[3][0]}')


check_levels()