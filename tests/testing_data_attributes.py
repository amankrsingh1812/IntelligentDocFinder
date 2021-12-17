class TestingData:
    DB_DIR = 'playground/lmdb_test/'
    all_tags = ['animal', 'color', 'greetings']
    paragraphs_embeddings = [['abcabc'], ['defdef']]
    
    tf_store = {
        'doc_id_1hello': 2,
        'doc_id_1goodbye': 3,
        'doc_id_1black': 1,
        'doc_id_2horse': 2,
        'doc_id_2goodbye': 1,
        'doc_id_2black': 1
    }

    nq_store = {
        'hello': 1,
        'goodbye': 2,
        'black': 2,
        'horse': 1
    }

    token_store = {
        'doc_id_1': ['hello', 'black', 'goodbye'],
        'doc_id_2': ['horse', 'black', 'goodbye']
    }

    doc_store = {
        'doc_id_1': {
            'file_path': DB_DIR + 'doc1',
            'tags': ['color', 'greetings'],
            'num_tokens': 6,
            'paragraphs_embeddings': paragraphs_embeddings[0]
        },
        'doc_id_2': {
            'file_path': DB_DIR + 'doc2',
            'tags': ['animal', 'color', 'greetings'],
            'num_tokens': 4,
            'paragraphs_embeddings': paragraphs_embeddings[1]
        }
    }