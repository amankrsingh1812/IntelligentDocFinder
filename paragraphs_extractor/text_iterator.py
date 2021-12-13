from utils import *
from paragraphs_extractor.file_iterator_interface import FileIteratorInterface

class TXTIterator(FileIteratorInterface):
    def __init__(self, filename):
        self.filename = filename        
        self.paragraphs = []
        
        with open(self.filename, "r") as fd:
            for para in fd:
                para = para.replace('\n', '')
                if para:
                    self.paragraphs.append(para)