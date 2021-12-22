from numpy import dot
import numpy
from numpy.linalg import norm
from database_access_object.lmdb_database_access_object import *


def get_cosine_sim(a,b):
    a = numpy.array(a)
    b = numpy.array(b)
    return dot(a, b)/(norm(a)*norm(b))


def get_cosine_similarity_with_doc(doc_paragraph_embeddings: list, query_embedding: list) -> float:
    csim  = -1
    for para_embedd in doc_paragraph_embeddings:
        csim = max(csim, get_cosine_sim(para_embedd, query_embedding))
    return csim
        

def get_docs_info(top_k_docs: list, query_embedding: list) -> list:
    dao = LMDBdao.get_dao()
    dao.open_session()

    docs_list = []
    for doc_id in top_k_docs:
        doc_attributes = dao.get_doc_attributes(doc_id)
        doc_paragraph_embeddings = doc_attributes['paragraphs_embeddings']
        csim = get_cosine_similarity_with_doc(doc_paragraph_embeddings, query_embedding)
        
        # delete paragraphs_embeddings from doc_attributes
        del doc_attributes['paragraphs_embeddings']
        
        docs_list.append((doc_attributes, csim))
        
    docs_list.sort(key = lambda x: -x[1]) 
    result_docs_list = [x[0] for x in docs_list]
    dao.close_session()
    
    return result_docs_list
