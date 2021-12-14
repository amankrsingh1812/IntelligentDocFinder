import string
import re
import nltk
from nltk.stem import WordNetLemmatizer

wordnet_lemmatizer = WordNetLemmatizer()
stopwords = nltk.corpus.stopwords.words('english')

def remove_punctuation_and_lowertext(text):
    punctuationfree="".join([i for i in text if i not in string.punctuation])
    return punctuationfree.to_lower()

def tokenize(text):
    tokens = re.split('W+',text)
    return tokens

def remove_stopwords(text):
    output= [i for i in text if i not in stopwords]
    return output

def lemmatizer(text):
    lemm_text = [wordnet_lemmatizer.lemmatize(word) for word in text]
    return lemm_text