import math
from database_access_object.lmdb_database_access_object import *

class BM25DocRanker:
    k1 = 1.64
    b = 0.75
    
    def __init__(self, query_tokens: set, lmdb_dir = '/workspace/doc-finder/lmdb_database/'):
        self.query_tokens = query_tokens
        
        self.dao = LMDBdao.get_dao(lmdb_dir)
        self.dao.open_session();
        
        self.doc_list = self.dao.get_doc_list()
        self.avg_doc_len = 0
        
        for (doc_id, doc_len) in self.doc_list:
            self.avg_doc_len += doc_len
        self.avg_doc_len /= max(len(self.doc_list), 1)
        
        self.nq_map = {}
        for token in query_tokens:
            self.nq_map[token] = self.dao.get_nq_token(token)
            
        self.dao.close_session()
        
    def __get_idf(self, curr_doc_len: int, nqi: int) -> float:
        idf = math.log((curr_doc_len - nqi + 0.5) / (nqi + 0.5) + 1)
        return idf
    
    def __compute_score(self, idf_qi: float, tf_qi: int, curr_doc_len: int):
        numerator = idf_qi * tf_qi * (BM25DocRanker.k1 + 1)
        denominator = tf_qi + BM25DocRanker.k1 * (1 - BM25DocRanker.b + BM25DocRanker.b * curr_doc_len / self.avg_doc_len)
        return  numerator / denominator

    def __calculate_bm25_score(self, doc_id: str, doc_len: int) -> float:
        bm25_score = 0
        self.dao.open_session();
        
        for token in self.query_tokens:
            tf  = self.dao.get_tf_token(token, doc_id)
            idf = self.__get_idf(doc_len, self.nq_map[token])
            bm25_score += self.__compute_score(idf, tf, doc_len)
            
        self.dao.close_session()
        return bm25_score

    def __get_doc_scores(self) -> list:
        doc_scores = []
        
        for doc_id, doc_len in self.doc_list:
            doc_scores.append((doc_id, self.__calculate_bm25_score(doc_id, doc_len)))
            
        return doc_scores

    def get_top_doc_ids(self, k: int) -> list:
        doc_scores = self.__get_doc_scores()
        topk_doc_ids = []
        
        # filter top k doc_ids as per scores
        doc_scores.sort(key = lambda x: -x[1]) 
        topk_doc_ids = [x[0] for x in doc_scores]
        topk_doc_ids = topk_doc_ids[ : min(k, len(topk_doc_ids))]
        
        return topk_doc_ids