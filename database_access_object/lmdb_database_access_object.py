from database_access_object.database_access_object_interface import DAOInterface
import lmdb, pickle, uuid

class LMDBdao(DAOInterface):
    stores = ['tf', 'nq', 'doc', 'token']
    
    def __init__(self, lmbd_dir = '/workspace/doc-finder/lmdb_database/'):
        print("[Testing]: init function invoked")
        self.lmdb_dir = lmbd_dir
        self.environment_name = self.lmdb_dir
        self.env = lmdb.Environment(self.environment_name, max_dbs=5)
        self.txn = None
        print("[Testing]: env created")
        # self.db_map = self.env.open_db("tf".encode())
        self.db_map = {store: self.env.open_db(store.encode()) 
                       for store in LMDBdao.stores}
        print("[Testing]: db_map created")
        
    def __del__(self):
        if self.txn  is not None:
            raise Exception('Transaction has not stopped')
        self.env.close()
        
        
    def __check_requirements(self):
        if self.txn is None:
            raise Exception('Cannot initiate transaction without starting session')
    
    
    def open_session(self, is_write_txn=False):
        self.txn = self.env.begin(write=is_write_txn)
    
    
    def close_session(self):
        if self.txn is None:
            raise Exception('Transaction has not started')
        self.txn.commit()
        self.txn = None
        
        
    def __add_tf_map(self, doc_id: str, tf_map: dict):
        cursor = self.txn.cursor(db=self.db_map['tf'])
        kv_pairs = [ ((doc_id + token).encode('ascii'), pickle.dumps(frequency)) 
                        for (token, frequency) in tf_map.items() ]
        cursor.putmulti(kv_pairs)
        cursor.close()
    
    
    def __update_nq(self, doc_id: str, tokens: list):
        self.__check_requirements()
        
        for token in tokens:
            nq_value = self.__get_nq_token(token) + 1
            self.txn.put(token.encode('ascii'), pickle.dumps(nq_value),
                         db=self.db_map['nq'])
            
        
    def add_document(self, file_path: str, paragraphs_embeddings: list, 
                     tags: list, num_tokens: int, tf_map: dict) -> str:
        self.__check_requirements()
        doc_id = str(uuid.uuid4())
        
        # Update TF related db
        self.__add_tf_map(doc_id, tf_map)
        
        # Update IDF related db
        self.__update_nq(doc_id, tf_map.keys())
        
        # Populate 'token' db using tf_maps
        self.txn.put(doc_id.encode('ascii'), pickle.dumps(list(tf_map.keys())), db=self.db_map['token'])
        
        # Update remaining data related to document
        doc_attributes = {
            'file_path': file_path,
            'tags': tags,
            'num_tokens': num_tokens,
            'paragraphs_embeddings': paragraphs_embeddings
        }
        self.txn.put(doc_id.encode('ascii'), pickle.dumps(doc_attributes), db=self.db_map['doc'])
        
        return doc_id
    
        
    def get_doc_list(self) -> list:
        self.__check_requirements()
        doc_list = [ (key.decode(), pickle.loads(doc_attributes)['num_tokens'])
                          for key, doc_attributes in self.txn.cursor(db=self.db_map['doc']) ]
                                                       # .iternext(keys=True, values=False) ]
        return doc_list
    
    
    def get_doc_attributes(self, doc_id: str) -> dict:
        self.__check_requirements()
        
        doc_data = self.txn.get(doc_id.encode('ascii'), db=self.db_map['doc'])
        if doc_data is None:
            return None
        
        doc_data = pickle.loads(doc_data)
        return doc_data
    
    
    def delete_document(self, doc_id: str) -> bool:
        self.__check_requirements()
        encoded_doc_id = doc_id.encode('ascii')

        # Decrement the count for affected tokens in nq store
        tokens_list = self.txn.get(encoded_doc_id, db=self.db_map['token'])
        tokens_list = pickle.loads(tokens_list)
        encoded_tokens = [ token.encode('ascii') for token in tokens_list ]
        cursor = self.txn.cursor(db=self.db_map['nq'])
        kv_pairs = cursor.getmulti(encoded_tokens)
        kv_pairs = [ (k, pickle.dumps(pickle.loads(v)-1)) for (k, v) in kv_pairs ]
        cursor.first()     # reset cursor to nq store
        cursor.putmulti(kv_pairs, overwrite=True)
        
        # Delete entries from tf store
        for token in tokens_list:
            self.txn.delete(encoded_doc_id + token.encode('ascii'), db=self.db_map['tf'])
        
        # Delete entry from token store 
        self.txn.delete(encoded_doc_id, db=self.db_map['token'])
        
        # Delete document from document store
        self.txn.delete(encoded_doc_id, db=self.db_map['doc'])
        
    
    def get_tf_token(self, token: str, doc_id: str) -> int:
        self.__check_requirements()
        
        token_id = (doc_id + token).encode('ascii')
        tf_value = self.txn.get(token_id, db=self.db_map['tf'], default=0)
        return tf_value if tf_value == 0 else pickle.loads(tf_value)
        
        
    def get_nq_token(self, token: str) -> int:
        self.__check_requirements()
        return self.__get_nq_token(token)
    
    
    def __get_nq_token(self, token: str) -> int:
        nq_value = self.txn.get(token.encode('ascii'), db=self.db_map['nq'], default=0)
        return nq_value if nq_value == 0 else pickle.loads(nq_value)