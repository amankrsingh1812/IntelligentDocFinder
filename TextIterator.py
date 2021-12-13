from utils import *

class TextIterator:
    def __init__(self, _filename):
        self.filename = _filename
        
    
    def __iter__(self):
        self.paragraphs = []
        self.index = 0
        with open(self.filename, "r") as fd:
            for para in fd:
                para = para.replace('\n', '')
                if para is not '' :
                    self.paragraphs.append(para)
        return self
        
    def __next__(self):
        if self.index < len(self.paragraphs):
            x = self.paragraphs[self.index]
            self.index += 1
            return x
        else:
            raise StopIteration
            
texti = TextIterator(html_to_text(filename('txt')))
count = 1                                                # For debugging
for para in iter(texti):
    print("Paragraph count = ", count, end=' ')          # For debugging
    count += 1                                           # For debugging 
    print(para)