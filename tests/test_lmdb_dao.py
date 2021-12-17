import unittest
from database_access_object.lmdb_database_access_object import *
import lmdb, os, shutil
from testing_data_attributes import TestingData 


def add_dict_to_txn(dct, txn, database):
    cursor = txn.cursor(db=database)
    kv_pairs = [ (key.encode('ascii'), pickle.dumps(val)) for (key, val) in dct.items() ]
    cursor.putmulti(kv_pairs)
    cursor.close()

    
def init_db():
    # doc_1: hello, black, goodbye, goodbye, hello, black
    # doc_2: horse, black, goodbye, horse
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
    

class LMDBdaoTest(unittest.TestCase):        
    def setUp(self):
        init_db()
        self.lmdbdao = LMDBdao(TestingData.DB_DIR)
    
    def test_get_tf_token(self):
        self.lmdbdao.open_session()
        doc_id = 'doc_id_1'
        token = 'hello'
        expected = 2
        
        token_tf = self.lmdbdao.get_tf_token(token, doc_id)
        self.assertEqual(token_tf, expected)
        self.lmdbdao.close_session()
        
    def test_get_nq_token(self):
        self.lmdbdao.open_session()
        token = 'hello'
        expected = 1
        
        self.assertEqual(self.lmdbdao.get_nq_token(token), expected)
        self.lmdbdao.close_session()
        
    def test_get_doc_list(self):
        self.lmdbdao.open_session()
        doc_list = self.lmdbdao.get_doc_list()
        expected_doc_list = [ (key, doc_attributes['num_tokens']) 
                             for key, doc_attributes in TestingData.doc_store.items() ]
        self.assertEqual(doc_list, expected_doc_list)
        self.lmdbdao.close_session()
    
    def test_add_document(self):
        self.lmdbdao.open_session(True)
        doc_store_entry = TestingData.doc_store['doc_id_1']
        
        tf_map = {
            'hello': 2,
            'goodbye': 3,
            'black': 1
        }
        doc_id = self.lmdbdao.add_document(doc_store_entry['file_path'],
                                  doc_store_entry['paragraphs_embeddings'], 
                                  doc_store_entry['tags'], 
                                  doc_store_entry['num_tokens'], 
                                  tf_map)
        
        # Close and then open the session to commit the transactions
        self.lmdbdao.close_session()
        self.lmdbdao.open_session()
        
        # Test doc_list
        doc_list = self.lmdbdao.get_doc_list()
        self.assertEqual(len(doc_list), 3)
        
        # Test nq_store
        self.assertEqual(self.lmdbdao.get_nq_token('hello'), 2)
        self.assertEqual(self.lmdbdao.get_nq_token('goodbye'), 3)
        self.assertEqual(self.lmdbdao.get_nq_token('black'), 3)
        
        # Test token_store
        self.assertEqual(self.lmdbdao.get_tf_token('hello', doc_id), 2)
        self.assertEqual(self.lmdbdao.get_tf_token('black', doc_id), 1)
        self.assertEqual(self.lmdbdao.get_tf_token('goodbye', doc_id), 3)
        
        self.lmdbdao.close_session()
        
    def test_delete_document(self):
        self.lmdbdao.open_session(True)
        doc_id = 'doc_id_1'
        self.lmdbdao.delete_document(doc_id)
        
        # Close and then open the session to commit the transactions
        self.lmdbdao.close_session()
        self.lmdbdao.open_session()
        
        expected = ('doc_id_2', TestingData.doc_store['doc_id_2']['num_tokens'])
        doc_list = self.lmdbdao.get_doc_list()
        
        # Test doc_list
        self.assertEqual(len(doc_list), 1)
        self.assertEqual(doc_list[0], expected)
        
        # Test nq_store
        self.assertEqual(self.lmdbdao.get_nq_token('hello'), 0)
        self.assertEqual(self.lmdbdao.get_nq_token('goodbye'), 1)
        self.assertEqual(self.lmdbdao.get_nq_token('black'), 1)
        self.assertEqual(self.lmdbdao.get_nq_token('horse'), 1)
        
        # Test token_store
        self.assertEqual(self.lmdbdao.get_tf_token('hello', 'doc_id_1'), 0)
        self.assertEqual(self.lmdbdao.get_tf_token('black', 'doc_id_1'), 0)
        self.assertEqual(self.lmdbdao.get_tf_token('goodbye', 'doc_id_1'), 0)
        self.assertEqual(self.lmdbdao.get_tf_token('horse', 'doc_id_2'), 2)
        self.assertEqual(self.lmdbdao.get_tf_token('goodbye', 'doc_id_2'), 1)
        self.assertEqual(self.lmdbdao.get_tf_token('black', 'doc_id_2'), 1)
        
        self.lmdbdao.close_session()
    
    def test_get_doc_attributes(self):
        self.lmdbdao.open_session()
        doc_id = 'doc_id_1'
        doc_attributes = self.lmdbdao.get_doc_attributes(doc_id)
        expected = TestingData.doc_store[doc_id]
        self.assertEqual(doc_attributes, expected)
        self.lmdbdao.close_session()
        
    def tearDown(self):
        print('\n[Testing]: Completed testing!!')
        del_db()
    
if __name__ == '__main__':
    unittest.main()