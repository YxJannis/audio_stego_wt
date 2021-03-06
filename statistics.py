import csv
from embedder import Embedder
from detector import Detector
from audio_file import AudioFile


class Statistics:
    """
    Extract statistics from audio file embedding and detection procedure
    """

    def __init__(self, output_file: str = "statistics.csv"):
        self.output_file = output_file
        self.header = ["embed_bit", "wavelet", "subtype", "error_rate", "audible"]
        self.full_data = [self.header]
        self.error_rate = None

    def process(self, embedder_obj: Embedder, detector_obj: Detector):
        """
        Extract information from embedder and detector objects to add to statistics csv
        """
        write_file_subtype = embedder_obj.write_file_subtype
        embed_bit = embedder_obj.embed_bit
        wavelet_type = embedder_obj.wavelet_type
        self.error_rate = AudioFile.check_error_rate(embedder_obj.message, detector_obj.detected_message)

        data = [embed_bit, wavelet_type, write_file_subtype, round(self.error_rate, 4), ' ']

        self.full_data.append(data)

    def write_csv(self):
        """
        Write data into structured csv file
        """
        with open(self.output_file, mode='w') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', )
            csv_writer.writerows(self.full_data)
        print(f'Writing completed.')


if __name__ == '__main__':
    input_f = 'input_files/SaChenPromenade1.wav'
    s = Statistics('statistics/statistics.csv')
    for i in range(1, 31):
        em_bit = i
        #e = Embedder(input_f, output_file_name=f'output_files/wt_bit{em_bit}_embedding_PCM16.wav',
        #             embed_bit=em_bit)
        #d = Detector(f'output_files/wt_bit{em_bit}_embedding_PCM16.wav', embed_bit=em_bit)
        #s.process(e, d)

        e = Embedder(input_f, output_file_name=f'output_files/wt_bit{em_bit}_embedding_PCM32.wav',
                     embed_bit=em_bit, write_file_subtype="PCM_32")
        #d = Detector(f'output_files/wt_bit{em_bit}_embedding.wav', embed_bit=em_bit)
        #s.process(e, d)
    #s.write_csv()
