from enum import Enum     
import numpy as np

Filetypes = Enum('File','txt pdf docx pptx')

def generate_filename(extension):
    """ 
    Returns sample file from the samples/ folder
    
    Arguments:
    extension - extension of the req doc
    """
    return f'samples/sample_{extension}.{extension}'

def calculate_cosine_similarity(a, b) -> float:
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))