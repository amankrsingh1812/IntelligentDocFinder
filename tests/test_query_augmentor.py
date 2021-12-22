from query_engine.query_augmentor import QueryEngine

def test_get_processed_augmented_tokens(query):
    query_engine = QueryEngine()
    preprocessed_tokens = query_engine.get_processed_augmented_tokens(query)
    print(preprocessed_tokens)

if __name__ == '__main__':
    query = 'Modern humans arrived on the Indian subcontinent from Africa no later than 1 years ago.'
    test_get_processed_augmented_tokens(query)