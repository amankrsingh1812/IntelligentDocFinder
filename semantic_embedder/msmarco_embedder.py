from sentence_transformers import SentenceTransformer
from semantic_embedder.semantic_embedder_interface import SemanticEmbedderInterface


class MSMARCOEmbedder(SemanticEmbedderInterface):
    embedder = None
    
    @staticmethod
    def get_embedder():
        if MSMARCOEmbedder.embedder is None:
            MSMARCOEmbedder.embedder = MSMARCOEmbedder()
        return MSMARCOEmbedder.embedder
    
    def __init__(self):
        self.model = SentenceTransformer('msmarco-distilbert-base-v4')

    def __encode_text(self, text):
        text_embedding = self.model.encode(text)
        return text_embedding

    def get_paragraph_embeddings(self, file_iterator) -> list:
        paragraph_embeddings = []
        
        for para in iter(file_iterator):
            encoded_para = self.__encode_text(para)
            paragraph_embeddings.append(encoded_para)
            
        return paragraph_embeddings
    
    def get_query_embeddings(self, query: str) -> list:
        return self.__encode_text(query)