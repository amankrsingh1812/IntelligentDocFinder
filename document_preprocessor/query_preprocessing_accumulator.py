from document_preprocessor.accumulator_interface import AccumulatorInterface

class QueryPreprocessingAccumulator(AccumulatorInterface):
    def __init__(self):
        self.tokens_set = set()
    
    def accumulate(self, data):
        for token in data:
            self.tokens_set.add(token)

    def get_result(self):
        return self.tokens_set
    