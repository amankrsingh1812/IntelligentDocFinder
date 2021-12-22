from transformers import BertTokenizer, BertModel
import pandas as pd
import numpy as np
import torch

from semantic_embedder.semantic_embedder_interface import SemanticEmbedderInterface

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
    
    def get_paragraph_encodings(self, file_iterator) -> list:
        paragraph_encodings = []
        
        for para in iter(file_iterator):
            encoded_para = __encode_text(para)
            paragraph_encodings.append(encoded_para)
            
        return paragraph_encodings
    
    def get_query_encoding(self, query: str) -> list:
        return self.__encode_text(query)
    
    def __encode_text(self, text: str) -> list:
        tokenized_text, tokens_tensor, segments_tensors = self.__bert_text_preparation(text, tokenizer)
        list_token_embeddings = self.__get_bert_embeddings(tokens_tensor, segments_tensors, model)

        # Find the position 'bank' in list of tokens
        word_index = tokenized_text.index('bank')
        
        # Get the embedding for bank
        word_embedding = list_token_embeddings[word_index]
        
        return word_embedding
    
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
    
    def __bert_text_preparation(text):
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