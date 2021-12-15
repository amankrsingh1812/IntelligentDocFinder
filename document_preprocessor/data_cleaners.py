import string
import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, word_tokenize

wordnet_lemmatizer = WordNetLemmatizer()
stopwords = nltk.corpus.stopwords.words('english')

def remove_punctuation(text: str) -> str:
    punctuation_free = "".join([i for i in text if i not in string.punctuation])
    return punctuation_free

def tokenize(text: str) -> list:
    tokens = text.split(' ')
    return tokens

def remove_stopwords(text: list) -> list:
    output = [i for i in text if i.lower() not in stopwords]
    return output

def lemmatizer_and_lowertext(text: list) -> list:
    lemma_text = []
    for (word, tag) in pos_tag(text):
        wntag = tag[0].lower()
        wntag = wntag if wntag in ['a', 'r', 'n', 'v'] else None
        lemma_text.append(
            wordnet_lemmatizer.lemmatize(word, wntag).lower() if wntag else word
        )
    return lemma_text