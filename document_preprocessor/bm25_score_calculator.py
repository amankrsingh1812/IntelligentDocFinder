k1 = 1.64
b = 0.75 
avg_doc_len = 123        # Retrieve avegrage doc length

score = {}
tf = {}
nq = {}
doc_len = {}
# idf = {}
doc_list = set()

def compute_tf(prargraph_tokens,doc_id):
    doc_list.add(doc_id)
    
    if doc_id not in tf:
        tf[doc_id]={}
        
    if doc not in doc_len:
        doc_len[doc_id]=0
        
    for token in tokens:
        if token not in tf[doc_id]:
            tf[doc_id][token]=0
        tf[doc_id][token]+=1
        
        doc_len[doc_id]+=1
        
        if token not in nq:
            nq[token]=set()
        nq[token].add(doc_id)
    
def get_idf(token):
    N = doc_list.size
    nqi = 0
    if token in nq:
        nqi=nq[token].size
    
    idf = math.log((N-nqi+0.5)/(nqi+0.5)+1)
    return idf

def compute_score(token,doc_id):
    if doc_id not in score:
        doc_id[score]={}
    
    idf_qi = get_idf(token)
    f_qi = tf[doc_id][token]
    D = doc_len[doc_id]
    
    doc_id[score][token] = lambda x: ((idf_qi*f_qi*(k1+1)/(f_qi+k1*(1 - b + b * D/x)))