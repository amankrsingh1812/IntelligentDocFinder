# 1. Retrieve query
# 2. Get tokens
# 3. Top k documents
# 4. Paragraph embeddings of original query
# 5. MSMARCO + cosine similarity
# 6. Return required documents

from query_engine.query_augmentor import QueryEngine
from document_preprocessor.bm25_doc_ranker import BM25DocRanker

def execute_query(query: str) -> list:
    query_engine = QueryEngine()
    preprocessed_tokens = query_engine.get_processed_augmented_tokens(query)

    bm25_doc_ranker = BM25DocRanker(preprocessed_tokens)
    top_k_docs = bm25_doc_ranker.get_top_doc_ids(k=2)

    # Apply 2nd level filtering
    # get_docs_info(top_k_docs, curr_query_embedding) 
        # -> [(cosine_sim, attributes without paragraph embeddings)]
        
    # get_csim_with_doc(doc_paragraph_embeddings, curr_query_embedding) -> float:
    
    # show_relevant_documents([(cosine_sim, attributes without paragraph embeddings)]) 