import re, string
import nltk, torch

import nlpaug.augmenter.word as naw
from nltk import pos_tag, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

from document_preprocessor.data_cleaners import *

class QueryEngine:
    """
    Used to convert raw input query to augmented,
    processed list of tokens which can be directly
    used for TF-IDF and BM25 score calculations
    """
    
    def __init__(self, top_k=10):
        nltk.download('stopwords')
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('maxent_treebank_pos_tagger')
        nltk.download('wordnet')
        nltk.download('omw-1.4')
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
        # Contextual Augmentor
        self.aug_word = naw.ContextualWordEmbsAug(top_k=top_k, device=self.device)
        
        # POS tagger
        self.treebank_tagger = nltk.data.load('taggers/maxent_treebank_pos_tagger/english.pickle')
    
    def __remove_numbers_from_query(self, query: str) -> str:
        # Normalise numbers in original query
        # Ex: 50, 000  --> 1
        query = re.sub(r'[0-9]+[\.,0-9]*', '1', query)
        query = re.sub(r'1[\ 1]*', '1 ', query)
        
        return query

    def __get_pos_tags(self, words: list) -> list:
        return self.treebank_tagger.tag(words)
    
    def __get_tokenized_augmented_query(self, query: str) -> list:
        # Tokenize the query
        tokenized_query = nltk.word_tokenize(query)
        query = " ".join(tokenized_query)
        
        # Restrict the replacement of proper nouns while augmenting
        restricted_positions = []
        for i, (word, tag) in enumerate(self.__get_pos_tags(tokenized_query)):
            # print(word,tag)
            if tag == 'NNP':
                restricted_positions.append(i)

        # Keep all augmented sentences together
        tokenized_augmented_query = [tokenized_query]
        augmented_sentences = self.aug_word.augment(query, n=len(tokenized_query)//5+3)
        
        for aug_sent in augmented_sentences:
            # print(aug_sent)
            tokenized_aug_sent = nltk.word_tokenize(aug_sent)
            tokenized_aug_sent = [ tokenized_query[i]
                                      if i in restricted_positions else tokenized_aug_sent[i] 
                                      for i in range(len(tokenized_aug_sent))]
            tokenized_augmented_query.append(tokenized_aug_sent)

        return tokenized_augmented_query
    
    def __run_on_augmented_sentences(self, tokens: list) -> set:
        lemmatized_tokens = lemmatizer_and_lowertext(tokens)
        punctuation_free_tokens = remove_punctuation(lemmatized_tokens)
        stopwords_free_tokens = remove_stopwords(punctuation_free_tokens)
        cleaned_tokens = stemm_text(stopwords_free_tokens)
        
        final_set = set()
        for token in cleaned_tokens:
            if token.isnumeric() == False:      # Remove numbers
                final_set.add(token)    
        
        return final_set
    
    def __remove_special_characters_from_query_tokens(self, tokens: list) -> list:
        cleaned_tokens = [token for token in tokens if re.match(r'[^\W\d]*$', token)]
        return cleaned_tokens

    def get_processed_augmented_tokens(self, query: str) -> set:
        # return set of pre-processed tokens generated by query augmentation
        
        processed_query = self.__remove_numbers_from_query(query)
        tokenized_augmented_query = self.__get_tokenized_augmented_query(processed_query)
        processed_augmented_query_tokens = self.__run_on_augmented_sentences(tokenized_augmented_query)
        cleaned_tokens = self.__remove_special_characters_from_query_tokens(processed_augmented_query_tokens)

        return cleaned_tokens