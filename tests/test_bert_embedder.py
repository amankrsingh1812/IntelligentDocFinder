from utils import *
from semantic_embedder.bert_embedder import BertEmbedder
from paragraphs_extractor.iterator_factory import IteratorFactory

import numpy as np

def test_get_paragraph_embeddings(file_iterator):
    bert_embedder = BertEmbedder.get_embedder()
    paragraph_embeddings = bert_embedder.get_paragraph_embeddings(file_iterator)
    print("[Paragraph]: ", np.shape(paragraph_embeddings))

def test_get_query_embeddings(query):
    bert_embedder = BertEmbedder.get_embedder()
    query_embeddings = bert_embedder.get_query_embeddings(query)
    return query_embeddings

if __name__ == '__main__':
    e1 = test_get_query_embeddings('modern humans arrived on the Indian subcontinent from Africa no later than 1 years ago.')
    e2 = test_get_query_embeddings('modern humans arrived on this indian continent from africa perhaps later that 1 years bp.')
    e3 = test_get_query_embeddings('islamic islam migrated around eastern indian subcontinent from africa no later than 1 years before.')

    print(calculate_cosine_similarity(e1, e2))
    print(calculate_cosine_similarity(e2, e3))
    print(calculate_cosine_similarity(e3, e1))
    
    # iterator = IteratorFactory.get_iterator(generate_filename("txt"), "txt")
    # test_get_paragraph_embeddings(iterator)