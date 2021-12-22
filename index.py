from executors.document_preprocessing_executor import insert_document
from executors.query_executor import execute_query
import os


if __name__ == '__main__':
    while 1:
        # os.system('clear')
        print('Enter number for operation:')
        print('[1] Add document to Intelligent Doc Finder')
        print('[2] Find relevant document with your query')
        print('[0] Exit application')
        operation = int(input())
        
        if operation == 1:                    # Add document
            file_path = input('Enter file path: ')
            extension = input('Enter file type: ')
            insert_document(file_path, extension)
            
        elif operation == 2:                  # Perform query
            query = input('Enter query: ')
            print("Searching for query", query)
            results = execute_query(query)
            print(results)
            
        else:
            break
             
"""
TODOs 

1. Add class for extracting PDFs

2. For DOCX read heading of file

3. For PPTX add logic to extract finer paragraphs
    from shapes in slides
    
4. Replace naive tokenizer with RegEx based tockenizer
   Ref - https://stackoverflow.com/questions/3845423/remove-empty-strings-from-a-list-of-strings
"""