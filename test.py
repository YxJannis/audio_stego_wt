from embedder import Embedder
from detector import Detector
from audio_file import AudioFile
from dwt_plotter import plot_master_2, plot_error_rates, plot_error_dist, plot_error_dist_2

# Goal: broad testing over range of embed_bits for different wavelet types to measure which wavelet type at which
# embedding bit is most robust & least audible


# https://en.wikipedia.org/wiki/Haar_wavelet
# https://en.wikipedia.org/wiki/Daubechies_wavelet
# discrete approximation of https://en.wikipedia.org/wiki/Meyer_wavelet
# https://en.wikipedia.org/wiki/Symlet
# https://en.wikipedia.org/wiki/Coiflet
# https://en.wikipedia.org/wiki/Biorthogonal_wavelet
wavelet_list = ['haar',
                'db2', 'db3', 'db4', 'db5', 'db6', 'db12', 'db16', 'db20', 'db30', 'db38',
                'dmey',
                'sym2', 'sym3', 'sym4', 'sym5', 'sym6', 'sym12', 'sym16', 'sym20',
                'coif1', 'coif2', 'coif10', 'coif16',
                'bior1.1', 'bior1.5', 'bior2.2', 'bior2.8', 'bior3.1', 'bior3.9', 'bior4.4', 'bior6.8'
                ]


input_file_small = 'input_files/file_example_WAV_2MG.wav'  # test file, much smaller file size
input_file = 'input_files/SaChenPromenade1.wav'
file_title = 'Promenade1'   # Use for plot file names saved on disc
seed = 1234                 # seed for pseudorandom message
message_length = 1726663 + 1000
message = AudioFile.generate_random_message(message_length, seed)


def generate_plots(file):
    for wavelet_type in wavelet_list:
        error_rates = {}
        for emb_bit in range(1, 17):
            # instantiate embedder who automatically creates output-file with message embedded (in channel 1)
            e = Embedder(file, wavelet_type=wavelet_type, msg=message,
                         output_file_name=f'output_files/test_output.wav', embed_bit=emb_bit)

            # instantiate detector that automatically reads in given file
            d = Detector(f'output_files/test_output.wav', embed_bit=emb_bit, wavelet_type=wavelet_type)

            # determine error rate of detected message
            error_rate = AudioFile.check_error_rate(e.message, d.detected_message)

            # plot
            plot_master_2(e, d, file_title, seed)
            error_rates[emb_bit] = error_rate

        plot_error_rates(error_rates, f'Error_Rates_{wavelet_type}')


def test_error_distribution(file, emb_bit, wavelet_type):
    """ Investigate how error-bits are distributed in detected message
    (do errors appear in blocks or scattered individually?) """
    # instantiate embedder who automatically creates output-file with message embedded (in channel 1)
    e = Embedder(file, wavelet_type=wavelet_type, msg=message,
                 output_file_name=f'output_files/test_output.wav', embed_bit=emb_bit)
    original_msg = message

    # instantiate detector that automatically reads in given file
    d = Detector(f'output_files/test_output.wav', embed_bit=emb_bit, wavelet_type=wavelet_type)
    detected_msg = d.detected_message

    # determine error rate of detected message
    error_rate = AudioFile.check_error_rate(e.message, d.detected_message)
    faulty_bits = []
    error_string = ''
    single_error = 0
    double_error = 0
    triple_error = 0
    flag = False
    double_flag = False
    for i in range(len(detected_msg)):
        if detected_msg[i] != original_msg[i]:
            single_error += 1
            #faulty_bits.append(1)
            error_string += '1'
            if double_flag:
                triple_error += 1
            if flag:
                double_error += 1
                double_flag = True
            flag = True
        else:
            #faulty_bits.append(0)
            error_string += '0'
            flag = False
            double_flag = False

    # plot_error_dist(faulty_bits, f'Error dist_{wavelet_type}, {emb_bit}')
    return error_rate, single_error, double_error, triple_error


small_wavelet_list = ['haar', 'db2', 'dmey', 'sym2', 'coif1', 'bior1.1']

for wavelet_type in small_wavelet_list:
    error_rates = []
    single_errors = []
    double_errors = []
    triple_errors = []
    embed_bits = [i for i in range(1, 17)]
    # embed_bits = [12, 13, 14, 15, 16]
    for emb_bit in embed_bits:
        er, se, de, te = test_error_distribution(input_file, emb_bit, wavelet_type)
        error_rates.append(er)
        single_errors.append(se)
        double_errors.append(de)
        triple_errors.append(te)
    plot_error_dist_2(error_rates, double_errors, triple_errors, embed_bits, f'error_analysis_{wavelet_type}')
    # plot_error_dist(single_errors, double_errors, triple_errors, embed_bits)

