import csv
from embedder import Embedder
from detector import Detector


class Statistics:
    """

    """

    def __init__(self, embedder_obj: Embedder, detector_obj: Detector):
        self.emb = Embedder
        self.det = Detector

        # relevant data:
        self.subtype = self.emb.cover_audio_file.write_file

    def extract_information(self):
        """
        Extract information from embedder and detector objects to add to statistics csv
        """

