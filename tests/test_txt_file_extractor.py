from utils import *
from paragraphs_extractor.iterator_factory import IteratorFactory

extensions = ['txt', 'docx', 'pptx', 'html']

for extension in extensions:
    print("EXTENSION: " + extension)
    iterator = IteratorFactory.get_iterator(generate_filename(extension), extension)
    count = 1
    
    for para in iter(iterator):
        print("Para #", count, end=' ')
        count += 1 
        print(para)
    print('\n')