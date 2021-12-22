from numpy import dot
import numpy
from numpy.linalg import norm
from semantic_embedder.msmarco_embedder import MSMARCOEmbedder

def test_get_query_embeddings(query):
    MSMARCO_embedder = MSMARCOEmbedder.get_embedder()
    query_embeddings = MSMARCO_embedder.get_query_embeddings(query)
    return query_embeddings

def get_cosine_sim(a,b):
    a = numpy.array(a)
    b = numpy.array(b)
    return dot(a, b)/(norm(a)*norm(b))

if __name__ == '__main__':
    e1 = test_get_query_embeddings('modern humans arrived on the Indian subcontinent from Africa no later than 1 years ago.')
    e2 = test_get_query_embeddings('modern humans arrived on this indian continent from africa perhaps later that 1 years bp.')
    e3 = test_get_query_embeddings('islamic islam migrated around eastern indian subcontinent from africa no later than 1 years before.')

    print(get_cosine_sim(e1,e2))
    print(get_cosine_sim(e2,e3))
    print(get_cosine_sim(e3,e1))