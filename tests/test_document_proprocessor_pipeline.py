from utils import *
from paragraphs_extractor.iterator_factory import IteratorFactory
from document_preprocessor.data_cleaners import *
from document_preprocessor.distributed_pipeline import *
from document_preprocessor.bm25_score_calculator import cal_tf


def test_txt_file():
    iterator = IteratorFactory.get_iterator(generate_filename("txt"), "txt")
    preprocess_pipeline = DistributedPipeline(file_iterator  =  iterator,
                                              stage_functions = [
                                                  remove_punctuation,
                                                  tokenize,
                                                  lemmatizer_and_lowertext,
                                                  remove_stopwords
                                              ], 
                                              accumulator = cal_tf)
    
    preprocessed_data = preprocess_pipeline.run()
    print("DONE")    
    print(preprocessed_data)    
    print("DONE")
    
test_txt_file()