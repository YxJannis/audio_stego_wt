import pywt
from audio_file import AudioFile

cover_audio_file = AudioFile('input_files/SaChenPromenade1.wav')
wavelet_type = 'db2'


# Keep in mind: Stereo audio has 2 channels therefore also two lists for each coeff (1 for each channel)
def multilevel_decomposition(level):
    data = pywt.wavedec(cover_audio_file.signal_data.T, wavelet=wavelet_type, level=level)
    return data


# print coefficients for decomposition of left channel
def print_coeffs(level):
    data = multilevel_decomposition(level)
    print(f'{data}')
    print(f'\n-----------\n{data[0][0]}')
    print(f'\n-----------\n{data[1][0]}')
    print(f'\n-----------\n{data[2][0]}')
    print(f'\n-----------\n{data[3][0]}')

