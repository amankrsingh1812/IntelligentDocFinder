from paragraphs_extractor.iterator_factory import IteratorFactory
from document_preprocessor.data_cleaners import *
from document_preprocessor.distributed_pipeline import *
from database_access_object.lmdb_database_access_object import *
from utils import Filetypes
from document_preprocessor.accumulator import DocPreprocessingAccumulator
from semantic_embedder.msmarco_embedder import MSMARCOEmbedder
from document_preprocessor.tag_assigner import assign_tags

def insert_document(file_name: str, file_path: str, extension: str, manual_tags: list):
    # Create iterator for file
    iterator = IteratorFactory.get_iterator(file_path, extension)
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
    doc_paragraphs_embeddings = MSMARCOEmbedder.get_embedder().get_paragraph_embeddings(file_iterator = iterator)
    
    # Create tags for the file
    tags = assign_tags(doc_paragraphs_embeddings)

    # Manual tagging
    tags.extend(manual_tags)

    # Insert document into database
    lmdbdao = LMDBdao.get_dao()
    lmdbdao.open_session(True)
    lmdbdao.add_document(file_name,
                         file_path,
                         doc_paragraphs_embeddings,
                         tags,
                         num_tokens,
                         tf_map)
    lmdbdao.close_session()