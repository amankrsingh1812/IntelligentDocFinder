class SemanticEmbedderInterface:
    def get_paragraph_encodings(self, file_iterator) -> list:
        pass
    
    def get_query_encoding(self, query: str) -> list:
        pass
