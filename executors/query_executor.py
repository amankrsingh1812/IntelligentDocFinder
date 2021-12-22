from query_engine.query_augmentor import QueryEngine
from document_preprocessor.bm25_doc_ranker import BM25DocRanker
from semantic_embedder.msmarco_embedder import MSMARCOEmbedder
from query_engine.semantic_sorter import get_docs_info

def execute_query(query: str) -> list:
    
    #Filter top k documents
    query_engine = QueryEngine()
    preprocessed_tokens = query_engine.get_processed_augmented_tokens(query)

    bm25_doc_ranker = BM25DocRanker(preprocessed_tokens)
    top_k_docs = bm25_doc_ranker.get_top_doc_ids(k=2)

    # Apply 2nd level filtering
    msmarco_embedder = MSMARCOEmbedder.get_embedder()
    query_embeddings = msmarco_embedder.get_query_embeddings(query)
    
    result_docs_list = get_docs_info(top_k_docs, query_embeddings)
    
    return result_docs_list