from document_preprocessor.accumulator_interface import AccumulatorInterface

class DocPreprocessingAccumulator(AccumulatorInterface):
    def __init__(self):
        self.doc_len = 0
        self.tf_map = {}
    
    def accumulate(self, data):
        self.doc_len += len(data)
        for token in data:
            if token in self.tf_map.keys():
                self.tf_map[token] += 1
            else:
                self.tf_map[token] = 1
                
    def get_result(self):
        return (self.tf_map, self.doc_len)
    