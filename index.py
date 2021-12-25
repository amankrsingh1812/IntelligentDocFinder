from executors.document_preprocessing_executor import insert_document
from executors.query_executor import *
from ipcqueue import posixmq
import sys, time, signal, os
from multiprocessing import shared_memory
import pickle
import json


def write_in_memory(buf, data):
    buf[:len(data)] = data
    

def handle_request(request_type, params):
    response = None
    
    if request_type == 1:
        insert_document(params['name'], params['path'], params['extension'], params['tags'])
        response = "200"
        
    elif request_type == 2:
        response = execute_query(params['query'])
        
    else:
        print('Query executed')
        response = execute_query_for_tags(params['name'])
        print('Query completed')

    return response


def main():
    message_queue = posixmq.Queue('/doc-phi-listener-queue', maxmsgsize=8192)
    while (1):
        try:
            if message_queue.qsize():
                
                request = message_queue.get()

                # Get request and pid for shared memory
                (request_type, request_parameters, pid) = request
                print('Type of request:\n', request_type)
                print('Client PID:', pid)

                response = handle_request(request_type, request_parameters)
                response = pickle.dumps(response)
                
                shm_client = shared_memory.SharedMemory(name='shm_'+str(pid), create=False)
                
                write_in_memory(shm_client.buf, response)
                
                shm_client.close()

                print('responded and waking client')
                os.kill(pid, signal.SIGCONT)
                # time.sleep(5)
        except:
            message_queue.close()
            shm_client.close()
            posixmq.unlink('/doc-phi-listener-queue')
            print('MQ deleted')
            sys.exit()
            
            
if __name__ == '__main__':
    main()
            
            
"""
TODOs 

1. Add class for extracting PDFs

2. For DOCX read heading of file

3. For PPTX add logic to extract finer paragraphs
    from shapes in slides
    
4. Replace naive tokenizer with RegEx based tockenizer
   Ref - https://stackoverflow.com/questions/3845423/remove-empty-strings-from-a-list-of-strings
"""