import unittest
from database_access_object.lmdb_database_access_object import LMDBdao
import lmdb, os, shutil, pickle
from testing_data_attributes import TestingData 
from document_preprocessor.bm25_doc_ranker import BM25DocRanker


def add_dict_to_txn(dct, txn, database):
    cursor = txn.cursor(db=database)
    kv_pairs = [ (key.encode('ascii'), pickle.dumps(val)) for (key, val) in dct.items() ]
    cursor.putmulti(kv_pairs)
    cursor.close()

    
def init_db():
    # doc_1: hello, black, goodbye, goodbye, hello, black
    # doc_2: horse, black, goodbye, horse
    # doc_3: science, science, science, science, science
    # doc_4: politics, politics, politics, politics, politics
    stores = ['tf', 'nq', 'doc', 'token']
    
    env = lmdb.Environment(TestingData.DB_DIR, max_dbs=5)
    
    print('[init_db]: env created')
    db_map = { store: env.open_db(store.encode()) for store in stores }
    
    print('[init_db]: dp_map created')
    txn = env.begin(write=True)
    for store in stores:
        add_dict_to_txn(eval('TestingData.' + store + '_store'), txn, db_map[store])
    
    print('[init_db]: commiting transactions')
    txn.commit()
    env.close()
    print('[init_db]: complete')

    
def del_db():
    print('[Testing]: Deleting the database')
    if os.path.exists(TestingData.DB_DIR):
        shutil.rmtree(TestingData.DB_DIR)
    

class BM25DocRankerTest(unittest.TestCase):
    def setUp(self):
        init_db()
    
    def test_get_top_doc_ids(self):
        queries = [ set(['science']), set(['politics']), set(['hello', 'goodbye']) ]
        k = 5
        
        result = []
        for query_set in queries:
            bm25_doc_ranker = BM25DocRanker(query_set, lmdb_dir = TestingData.DB_DIR)
            top_k_docs = bm25_doc_ranker.get_top_doc_ids(k)
            print(top_k_docs)
            result.append(top_k_docs)
            del bm25_doc_ranker
        
        
    def tearDown(self):
        print('\n[Testing]: Completed testing!!')
        del_db()
    
if __name__ == '__main__':
    unittest.main()