import math

k1 = 1.64
b = 0.75 
avg_doc_len = 123        # Retrieve average doc length

score = {}
tf = {}
nq = {}                  # nq[token] = set(docs containing that token at least once)
doc_len = {}
# idf = {}
doc_list = set()
import math

def compute_tf(paragraph_tokens, doc_id):
    doc_list.add(doc_id)
    
    if doc_id not in tf:
        tf[doc_id] = {}
        
    if doc not in doc_len:
        doc_len[doc_id] = 0
        
    for token in paragraph_tokens:
        if token not in tf[doc_id]:
            tf[doc_id][token]=0
        tf[doc_id][token]+=1
        
        doc_len[doc_id]+=1
        
        if token not in nq:
            nq[token]=set()
        nq[token].add(doc_id)
    
def get_idf(token: str) -> float:
    N = len(doc_list)
    nqi = len(nq[token]) if token in nq else 0
    
    idf = math.log((N-nqi+0.5)/(nqi+0.5)+1)
    return idf

def compute_score(token: str, doc_id: str):
    if doc_id not in score:
        doc_id[score] = {}
    
    idf_qi = get_idf(token)
    f_qi = tf[doc_id][token]
    D = doc_len[doc_id]
    
    doc_id[score][token] = lambda x: ((idf_qi*f_qi*(k1+1)/(f_qi+k1*(1 - b + b * D/x))))
    