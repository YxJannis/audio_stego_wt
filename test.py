from embedder import Embedder
from detector import Detector
from statistics import Statistics
import dwt_plotter

# Goal: broad testing over range of embed_bits for different wavelet types to measure which wavelet type at which
# embedding bit is most robust & least audible

input_f = 'input_files/SaChenPromenade1.wav'
em_bit = 12
message = ''.ljust(1726662+1, '1')      # message to be embedded (here: just 1s)

# instantiate embedder who automatically creates output-file with output_file_name with message embedded (in channel 1)
e = Embedder(input_f, msg=message, output_file_name=f'output_files/test_output.wav',
             embed_bit=em_bit)

# instantiate detector that automatically reads in given file
d = Detector(f'output_files/test_output.wav', embed_bit=em_bit)

# instantiate statistics object to get error rate, etc.
s = Statistics('statistics/test_stats.csv')
s.process(e, d)
print(f'\nError Rate: {s.error_rate}\n')                       # print error rate

### get difference in signal data (for channel 1)
original_data = e.cover_audio_file.signal_data.T[0]      # index [0] to get 1st channel
marked_data = d.audio_file.signal_data.T[0]              # index [0] to get 1st channel

data_diff = abs(original_data - marked_data)

print(f'\n\n--------\nOG data: {original_data}\nMarked data: {marked_data}\nData difference: {data_diff}\n--------\n')


### get differences in detail coefficients (for channel 1)
# detail coefficients before embedding (alias og):
original_dcoeffs = e.detail_coeffs[0]

# detail coefficients directly after embedding (alias emb):
embedded_dcoeffs = e.marked_detail_coeffs[0]

# detail coefficients of marked file after reading it (alias det)
detected_dcoeffs = d.detail_coeffs[0]

print(f'\n\n--------\nOriginal Detail coeffs: {original_dcoeffs}\nDetail coeffs directly after embedding: '
      f'{embedded_dcoeffs}\nDetail coeffs after detecting: {detected_dcoeffs}\n')

diff_og_emb = abs(original_dcoeffs - embedded_dcoeffs)
diff_og_det = abs(original_dcoeffs - detected_dcoeffs)
diff_emb_det = abs(embedded_dcoeffs - detected_dcoeffs)

print(f'Difference between original and embedded detail coeffs:\n{diff_og_emb}')
print(f'Difference between original and detected detail coeffs:\n{diff_og_det}')
print(f'Difference between embedded and detected detail coeffs:\n{diff_emb_det}')

dwt_plotter.plot_diff(diff_og_emb)
dwt_plotter.plot_diff(diff_og_det)
dwt_plotter.plot_diff(diff_emb_det)
