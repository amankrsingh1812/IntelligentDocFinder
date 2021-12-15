import string
import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, word_tokenize
from nltk.stem.porter import PorterStemmer

wordnet_lemmatizer = WordNetLemmatizer()
stopwords = nltk.corpus.stopwords.words('english')
ps = PorterStemmer()


def remove_punctuation(text: list) -> list:
    punctuation_free = [i for i in text if i not in string.punctuation]
    return punctuation_free


def tokenize(text: str) -> list:
    tokens = [nltk.word_tokenize(sentence) for sentence in  nltk.sent_tokenize(text)]
    return tokens


def remove_stopwords(text: list) -> list:
    output = [i for i in text if i.lower() not in stopwords]
    return output


def lemmatizer_and_lowertext(text: list) -> list:
    lemma_text = []
    for sentence in text:
        for (word, tag) in pos_tag(sentence):
            wntag = tag[0].lower()
            wntag = wntag if wntag in ['a', 'r', 'n', 'v'] else None
            lemma_text.append(
                wordnet_lemmatizer.lemmatize(word, wntag).lower() if wntag else word
            )
    return lemma_text


def stemm_text(text: list) -> list:    
    stemmed_text = [ps.stem(word) for word in text]
    return stemmed_text