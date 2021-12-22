from utils import *
from semantic_embedder.bert_embedder import BertEmbedder
from paragraphs_extractor.iterator_factory import IteratorFactory

import numpy as np

def test_get_paragraph_embeddings(file_iterator):
    bert_embedder = BertEmbedder.get_embedder()
    paragraph_embeddings = bert_embedder.get_paragraph_embeddings(file_iterator)
    print(paragraph_embeddings)

def test_get_query_embeddings(query):
    bert_embedder = BertEmbedder.get_embedder()
    query_embeddings = bert_embedder.get_query_embeddings(query)
    print(query_embeddings)

if __name__ == '__main__':
    # query = 'Modern humans arrived on the Indian subcontinent from Africa no later than 1 years ago.'
    # test_get_query_embeddings(query)
    
    iterator = IteratorFactory.get_iterator(generate_filename("txt"), "txt")
    test_get_paragraph_embeddings(iterator)