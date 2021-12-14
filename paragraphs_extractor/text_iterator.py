from utils import *
from paragraphs_extractor.file_iterator_interface import FileIteratorInterface

class TXTIterator(FileIteratorInterface):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        
        with open(self.filename, "r") as fd:
            for para in fd:
                para = para.replace('\n', '')
                if para:
                    self.paragraphs.append(para)