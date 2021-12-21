from document_preprocessor.data_cleaners import *
from document_preprocessor.query_preprocessing_accumulator import QueryPreprocessingAccumulator

def test_txt_file():
    sentence = 'Modern humans arrived on the Indian subcontinent from Africa no later than 55,000 years ago.'
    query_preprocessing_accumulator = QueryPreprocessingAccumulator()
    tokens = tokenize(sentence)
    clean_tokens = stemm_text(
        remove_stopwords(
            remove_punctuation(
                lemmatizer_and_lowertext(
                    tokens
                )
            )
        )
    )
    query_preprocessing_accumulator.accumulate(clean_tokens)
    print(query_preprocessing_accumulator.get_result())
    
test_txt_file()