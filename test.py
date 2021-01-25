from embedder import Embedder
from detector import Detector
from statistics import Statistics
import dwt_plotter

# Goal: broad testing over range of embed_bits for different wavelet types to measure which wavelet type at which
# embedding bit is most robust & least audible

input_f = 'input_files/SaChenPromenade1.wav'
file_title = 'Promenade1'
em_bit = 12
wavelet_type = 'db2'
error_rates = []
#message = ''.ljust(1726662+1, '1')      # message to be embedded (here: just 1s)
message = "".join([str(i % 2) for i in range(1726663)])     # Message with alternating 0s and 1s (01010101...)

# instantiate embedder who automatically creates output-file with output_file_name with message embedded (in channel 1)
e = Embedder(input_f, wavelet_type= wavelet_type, msg=message, output_file_name=f'output_files/test_output.wav',
             embed_bit=em_bit)

# instantiate detector that automatically reads in given file
d = Detector(f'output_files/test_output.wav', embed_bit=em_bit)

# instantiate statistics object to get error rate, etc.
s = Statistics('statistics/test_stats.csv')
s.process(e, d)

print(f'\nError Rate: {s.error_rate}\n')                       # print error rate


### Try out different wavelet types: https://en.wikipedia.org/wiki/Wavelet#List_of_wavelets
# TODO: plot error rate over all embed bits for each wavelet
# for wavelet in wavelet_types():
    #for embed bit in range(1,30)
        #plot_master2()
        #save error rate
    # plot (error rate)

dwt_plotter.plot_master_2(e, d, file_title)

