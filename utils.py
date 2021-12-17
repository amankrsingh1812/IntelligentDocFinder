from enum import Enum     

def generate_filename(extension):
    """ 
    Returns sample file from the samples/ folder
    
    Arguments:
    extension - extension of the req doc
    """
    return f'samples/sample_{extension}.{extension}'

Filetypes = Enum('File','txt pdf docx pptx')