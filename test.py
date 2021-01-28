from embedder import Embedder
from detector import Detector
from audio_file import AudioFile
from dwt_plotter import plot_master_2, plot_values

# Goal: broad testing over range of embed_bits for different wavelet types to measure which wavelet type at which
# embedding bit is most robust & least audible


# https://en.wikipedia.org/wiki/Haar_wavelet
# https://en.wikipedia.org/wiki/Daubechies_wavelet
# discrete approximation of https://en.wikipedia.org/wiki/Meyer_wavelet
# https://en.wikipedia.org/wiki/Symlet
# https://en.wikipedia.org/wiki/Coiflet
# https://en.wikipedia.org/wiki/Biorthogonal_wavelet
# https://en.wikipedia.org/wiki/Morlet_wavelet (continuous?)
wavelet_list = ['haar',
                'db2', 'db3', 'db4', 'db5', 'db6', 'db12', 'db16', 'db20', 'db30', 'db38',
                'dmey',
                'sym2', 'sym3', 'sym4', 'sym5', 'sym6', 'sym12', 'sym16', 'sym20'
                'coif1', 'coif2', 'coif10', 'coif16',
                'bior1.1', 'bior1.5', 'bior2.2', 'bior2.8', 'bior3.1', 'bior3.9', 'bior4.4', 'bior6.8',
                'morl'
                ]


input_f = 'input_files/SaChenPromenade1.wav'
file_title = 'Promenade1'
message = "".join([str(i % 2) for i in range(1726663 + 1000)])     # Message with alternating 0s and 1s (01010101...)


for wavelet_type in wavelet_list:
    error_rates = {}
    for emb_bit in range(1, 4):
        # instantiate embedder who automatically creates output-file with message embedded (in channel 1)
        e = Embedder(input_f, wavelet_type=wavelet_type, msg=message, output_file_name=f'output_files/test_output.wav',
                     embed_bit=emb_bit)

        # instantiate detector that automatically reads in given file
        d = Detector(f'output_files/test_output.wav', embed_bit=emb_bit, wavelet_type=wavelet_type)

        # determine error rate of detector
        error_rate = AudioFile.check_error_rate(e.message, d.detected_message)

        # plot
        plot_master_2(e, d, file_title)
        error_rates[emb_bit] = error_rate

    plot_values(error_rates, f'Error_Rates_{wavelet_type}')


