from paragraphs_extractor.iterator_factory import IteratorFactory
from document_preprocessor.data_cleaners import *
from document_preprocessor.distributed_pipeline import *
from database_access_object.lmdb_database_access_object import *
from utils import Filetypes
from document_preprocessor.accumulator import DocPreprocessingAccumulator

def insert_document(filepath: str, extension: Filetypes):
    # Create iterator for file
    iterator = IteratorFactory.get_iterator(filepath, extension)
    doc_preprocessing_accumulator = DocPreprocessingAccumulator()

    # Compute tf mapping for file
    preprocess_pipeline = DistributedPipeline(file_iterator = iterator,
                                              stage_functions = [
                                                  tokenize,
                                                  lemmatizer_and_lowertext,
                                                  remove_punctuation,
                                                  remove_stopwords,
                                                  stemm_text,
                                              ], 
                                              accumulator = doc_preprocessing_accumulator)
    
    tf_map, num_tokens = preprocess_pipeline.run()
    
    # Compute sentence embeddings 
    # TODO
    paragraphs_embeddings = BertEmbedder.get_embedder().get_paragraph_encodings(file_iterator = iterator)
    # paragraphs_embeddings = []
    
    # Create tags for the file
    # TODO
    # tags = create_tags(file_iterator = iterator)
    tags = []

    # TODO(low priority): manual tagging
    
    # Insert document into database
    lmdbdao = LMDBdao.get_dao(BASE_DIR)
    lmdbdao.open_session(True)
    lmdbdao.add_document(filepath,
                         paragraphs_embeddings,
                         tags,
                         num_tokens,
                         tf_map)
    lmdbdao.close_session()