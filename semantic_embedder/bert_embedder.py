from transformers import BertTokenizer, BertModel
import pandas as pd
import numpy as np
import torch
from collections import defaultdict

from semantic_embedder.semantic_embedder_interface import SemanticEmbedderInterface
from sklearn.feature_extraction.text import TfidfVectorizer

class BertEmbedder(SemanticEmbedderInterface):
    embedder = None
    
    @staticmethod
    def get_embedder():
        if BertEmbedder.embedder is None:
            BertEmbedder.embedder = BertEmbedder()
        return BertEmbedder.embedder
    
    def __init__(self):
        # Load the pre-trained BERT model
        # Embeddings will be derived from the outputs of this model
        self.model = BertModel.from_pretrained('bert-base-uncased',
                                               output_hidden_states = True)
        
        # Set up the tokenizer
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    
    def get_paragraph_embeddings(self, file_iterator) -> list:
        paragraph_embeddings = []
        
        for para in iter(file_iterator):
            encoded_para = self.__encode_text(para.split(" "))
            paragraph_embeddings.append(encoded_para)
            
        return paragraph_embeddings
    
    def get_query_embeddings(self, query: str) -> list:
        return self.__encode_text(query)

    def __encode_text(self, text: str) -> list:
        list_token_embeddings = [self.__get_word_embeddings(word) for word in text]
        dim = len(list_token_embeddings)

        vectorizer = TfidfVectorizer()
        vectorizer.fit(text)
        max_idf = max(vectorizer.idf_)

        weights = defaultdict( lambda: max_idf, [(w, vectorizer.idf_[i]) 
                                                for w, i in vectorizer.vocabulary_.items()])
        paragraph_embedding = np.array([
                                np.mean([list_token_embeddings[w] * weights[w]
                                        for w in words if w in list_token_embeddings])
                                for words in text
                                ])
                                
        paragraph_embedding = np.mean(np.array(list_token_embeddings))
        return paragraph_embedding

    def __get_word_embeddings(self, text) -> list:
        tokenized_text, tokens_tensor, segments_tensors = self.__bert_text_preparation(text)
        list_token_embeddings = self.__get_bert_embeddings(tokens_tensor, segments_tensors)
        
        return list_token_embeddings
    
    def __get_bert_embeddings(self, tokens_tensor, segments_tensors):
        """Get embeddings from an embedding model

        Args:
            tokens_tensor (obj)    : Torch tensor size [n_tokens]
                                     with token ids for each token in text
            segments_tensors (obj) : Torch tensor size [n_tokens]
                                     with segment ids for each token in text
            model (obj)            : Embedding model to generate embeddings
                                     from token and segment ids

        Returns:
            list: List of list of floats of size
                  [n_tokens, n_embedding_dimensions]
                  containing embeddings for each token

        """

        # Gradient calculation is disabled
        # Model is in inference mode
        with torch.no_grad():
            outputs = self.model(tokens_tensor, segments_tensors)
            # Remove the first hidden state
            # The first state is the input state
            hidden_states = outputs[2][1:]

        # Get embeddings from the final BERT layer
        token_embeddings = hidden_states[-1]
        
        # Collapse the tensor into 1-dimension
        token_embeddings = torch.squeeze(token_embeddings, dim=0)
        
        # Convert torchtensors to lists
        list_token_embeddings = [token_embed.tolist() for token_embed in token_embeddings]

        return list_token_embeddings
    
    def __bert_text_preparation(self, text):
        """Preparing the input for BERT

        Takes a string argument and performs
        pre-processing like adding special tokens,
        tokenization, tokens to ids, and tokens to
        segment ids. All tokens are mapped to seg-
        ment id = 1.

        Args:
            text (str)      : Text to be converted
            tokenizer (obj) : Tokenizer object
                              to convert text into BERT-re-
                              adable tokens and ids

        Returns:
            list : List of BERT-readable tokens
            obj  : Torch tensor with token ids
            obj  : Torch tensor segment ids


        """
        marked_text = "[CLS] " + text + " [SEP]"
        tokenized_text = self.tokenizer.tokenize(marked_text)
        indexed_tokens = self.tokenizer.convert_tokens_to_ids(tokenized_text)
        segments_ids = [1] * len(indexed_tokens)

        # Convert inputs to PyTorch tensors
        tokens_tensor = torch.tensor([indexed_tokens])
        segments_tensors = torch.tensor([segments_ids])

        return tokenized_text, tokens_tensor, segments_tensors