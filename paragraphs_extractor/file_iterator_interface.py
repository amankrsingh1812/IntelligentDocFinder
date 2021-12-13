class FileIteratorInterface:
    """ 
    Attributes:
        paragraphs: list of extracted paragraphs
        index: index of the current paragraph in the paragraphs list
    """
    
    def __init__(self):
        self.paragraphs = []
    
    def __iter__(self):
        self.index = 0
        return self
        
    def __next__(self):
        if self.index < len(self.paragraphs):
            x = self.paragraphs[self.index]
            self.index += 1
            return x
        else:
            raise StopIteration