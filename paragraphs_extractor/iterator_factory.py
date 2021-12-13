from paragraphs_extractor import *

class IteratorFactory:
    
    @staticmethod
    def get_iterator(filename, iterator_type):
        switcher = {
            'txt': text_iterator.TXTIterator,
            'pptx': pptx_iterator.PPTXIterator,
            'docx': docx_iterator.DOCXIterator,
            'html': html_iterator.HTMLIterator
        }
        
        return switcher[iterator_type](filename)