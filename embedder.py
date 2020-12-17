import random
import pywt
import librosa
from scipy.io import wavfile
from audio_file import AudioFile


class Embedder:
    def __init__(self, audio_file: AudioFile, wavelet_type: str = "db2", msg: str = None):
        self.wavelet_type = wavelet_type
        self.audio_file = audio_file
        self.signal_size = self.audio_file.size

        # message size handling
        if msg is None:
            self.message = self.generate_random_message(self.signal_size)
        else:
            if len(msg) != self.signal_size:
                print("Message has to be of length/size " + str(self.signal_size) +
                      ". Generating file with random message.")
                self.message = self.generate_random_message(self.signal_size)
            else:
                self.message = msg

        self.approx_coeffs = None
        self.detail_coeffs = None
        self.marked_detail_coeffs = None
        self.embed()
        self.reconstruct_audio()

    def generate_random_message(self, message_length):
        # generate message of length 'message_length'
        random_int = random.randint(0, 2**message_length - 1)

        # random string
        msg = '{0:b}'.format(random_int).zfill(message_length)

        # uncomment for string with only 1s
        #msg = ""
        #for i in range(self.signal_size):
        #    msg = msg + '1'

        #uncomment for string with only 0s
        # msg = ''.zfill(message_length)

        return msg

    def embed(self):
        # dwt on audio_file
        self.approx_coeffs, self.detail_coeffs = self.audio_file.dwt(self.wavelet_type)
        # TODO: detail_coefficients array struktur durchschauen, warum ist das array so aufgebaut?
        #  dwt benötigt EIGTL 2 Parameter. Data (input signal [array_like]) und wavelet (object oder name)
        #  optional sind: Modes (Signal extension modes, siehe https://pywavelets.readthedocs.io/en/latest/ref/signal-extension-modes.html#ref-modes)
        #  und die axis, über welche die dwt berechnet werden sollen.
        self.marked_detail_coeffs = self.detail_coeffs
        print(self.detail_coeffs)

        # embed message bit sequentially into each detail coefficient
        # TODO: embedden wir richtig?
        for i in range(0, len(self.detail_coeffs)-1):
            self.marked_detail_coeffs[i][0] = self.detail_coeffs[i][0] + int(self.message[i])
            # self.marked_detail_coeffs[i][1] = self.detail_coeffs[i][1] + int(self.message[i])
            # self.marked_detail_coeffs[i][2] = self.detail_coeffs[i][2] + int(self.message[i])
        print(self.marked_detail_coeffs)

    def reconstruct_audio(self):
        """ reconstruct the watermarked audio using idwt """
        reconstructed_signal = pywt.idwt(self.approx_coeffs, self.marked_detail_coeffs, self.wavelet_type)
        # TODO: astype('int16') rundet evtl? Runden von unseren float-values macht keinen Sinn
        #  wenn wir noch detecten wollen. Mit type 'float32' kommt das extrem "laute" Signal zustande.
        #  Vlt. ist scipy.io.wavfile die falsche library. Evtl. mit Librosa probieren.
        wavfile.write("wtmrkd_signal.wav", self.audio_file.sampling_frequency, reconstructed_signal.astype('int16'))
        # librosa.output.write_wav(path, self.audiosignal, self.samplerate) audiosignal = mono or stereo, samplerate als int, norm für die amplitute [-1,1]
        # TODO replace output.write_wav mit soundfile.write, da write_wav mit Librosa 0.8 entfernt wird
        #  .load(path, samplerate, mono, offset, duration)
        # self.audiosignal, self.samplerate = librosa.load(path, mono=True, samplerate=00000, offset=..., duration=...) Siehe audio.py ,default samplerate=22050


if __name__ == '__main__':
    sa_chen_promenade = AudioFile('SaChenPromenade1.wav')
    Embedder(sa_chen_promenade)
