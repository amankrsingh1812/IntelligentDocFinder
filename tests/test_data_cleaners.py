from document_preprocessor.data_cleaners import *

lemmatized = lemmatizer_and_lowertext('They were horsing around He was searching surrogates'.split(' '))
print(lemmatized)
# ['They', 'be', 'horse', 'around']
# ['They', 'be', 'horse', 'around', 'He', 'be', 'search', 'surrogate']
