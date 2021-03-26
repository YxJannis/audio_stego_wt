from pywt import wavedec, downcoef, waverec
from audio_file import AudioFile
import numpy as np


def decomposition(audio_file: AudioFile, level: int = 1, wavelet_type: str = 'db2', print_out: bool = False):
    """
    Multilevel 1D decomposition of audio data using discrete wavelet transform (dwt).

    Parameters
    ----------
    audio_file: AudioFile object
        Audio file for decomposition
    level: int
        depth of decomposition
    wavelet_type: str
        specific wavelet type for dwt
    print_out: bool
        print overview of detail coefficients for each level on console

    Returns
    -------
    [[cA_n, cD_n, cD_n-1, ..., cD2, cD1],[cD_level]]: list
        list of size level +1 containing approximation coefficients and
        detail coefficients of each level, specific detail coefficients for level
    """
    sig_data = np.array(audio_file.signal_data)
    if len(sig_data.shape) > 1:  # check if more than one channel exists, select first channel if so
        signal_data = audio_file.signal_data[0]
    else:
        signal_data = audio_file.signal_data
    full_data = wavedec(data=signal_data, wavelet=wavelet_type, level=level)
    if print_out:
        print(f'\n\n-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-'
              f'+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+'
              f'\nDecomposition for level {level}:\n\n')
        print(f'Approximation coefficients:\n {full_data[0]}\n\n')
        print(f'Detail coefficients:\n')
        for j in range(level):
            print(f'Level {level - j}:')
            print(f'Array size: {len(full_data[j + 1])}')
            print(f'{full_data[j + 1]}\n')
    dc_at_level = downcoef(part='d', data=signal_data, wavelet=wavelet_type, level=level)
    return full_data, dc_at_level


def get_detail_coeffs_for_lvl(signal_data, wavelet_type: str = 'db2', level: int = 1):
    """
    Get detail coefficients at specific level only.

    Parameters
    ----------
    signal_data: array_like
        signal data from original audio
    wavelet_type: str
        specific wavelet type for dwt
    level: int
        level for decomposition

    Returns
    -------
        detail coefficients at level
    """
    return downcoef(part='d', data=signal_data, wavelet=wavelet_type, level=level)


def reconstruct_w_modified_dcoeffs(full_coeffs, mod_dcoeffs, wavelet_type: str = 'db2', level: int = 1):
    """
    Reconstruct audio using inverse dwt with modified detail coefficients from specified level.

    Parameters
    ----------
    full_coeffs: array_like
        All coefficients from multilevel decomposition
         (approximation coefficients and detail coefficients for each level)
    mod_dcoeffs: array_like
        Modified detail coefficients at specified level
    wavelet_type:
        specific wavelet type for idwt
    level: int
        decomposition level of modified detail coefficients

    Returns
    -------
    signal_data: list
        Reconstructed audio file

    """
    full_coeffs[-level] = mod_dcoeffs
    return waverec(coeffs=full_coeffs, wavelet=wavelet_type)


if __name__ == '__main__':
    # HowTo:
    # Initialize cover AudioFile
    # cover_audio_file = AudioFile('input_files/SaChenPromenade1.wav')
    cover_audio_file = AudioFile('input_files/file_example_WAV_2MG.wav')

    # specify wavelet type and desired decomposition depth/level ('db2' can be used as default)
    wavelet = 'haar'
    decomposition_level = 2

    print(f'original audio:\n{cover_audio_file.signal_data[0]}')

    # perform decomposition
    all_coeffs, dc = decomposition(cover_audio_file, wavelet_type=wavelet, level=decomposition_level, print_out=False)

    # TODO: modify detail coefficients dc (e.g. by embedding in them)
    modified_dc = dc

    # reconstruct audio file by passing unmodified coefficients (all_coeffs) and modified detail coefficients from
    # decomposition_level (modified_dc) to function
    reconstructed_audio = reconstruct_w_modified_dcoeffs(all_coeffs, modified_dc, level=decomposition_level,
                                                         wavelet_type=wavelet)

    print(f'Reconstructed audio:\n{reconstructed_audio}')

    # enjoy the reconstructed audio
