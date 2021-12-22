class SemanticEmbedderInterface:
    def get_paragraph_embeddings(self, file_iterator) -> list:
        pass
    
    def get_query_embeddings(self, query: str) -> list:
        pass
