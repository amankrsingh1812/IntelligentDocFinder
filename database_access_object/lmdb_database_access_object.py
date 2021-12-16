from database_access_object_interface import dao_interface
import lmdb, pickle, uuid

class lmdb_dao(dao_interface):
    stores = ['tf', 'nq', 'doc', 'token']
    
    def __init__(self):
        self.lmdb_dir = '/workspace/doc-finder/lmdb_database/'
        self.environment_name = self.lmdb_dir
        self.env = lmdb.Environment(self.environment_name, max_dbs=5)
        self.txn = None
        self.db_map = {store: self.env.open_db(store.encode("ascii")) 
                       for store in lmdb_dao.stores}
        
        
    def __del__(self):
        if self.txn  is not None:
            raise Exception('Transaction has not stopped')
        self.env.close()
    
    
    def __check_requirements(self):
        if self.txn is None:
            raise Exception('Cannot initiate transaction without starting session')
    
    
    def open_session(self, is_write_txn = False):
        self.txn = self.env.begin(is_write_txn)
    
    
    def close_session(self):
        if self.txn  is not None:
            raise Exception('Transaction has not started')
        self.txn.commit()
        self.txn = None
        
        
    def __add_tf_map(self, doc_id: str, tf_map: dict):
        for (token, frequency) in tf_map:
            combined_key = (doc_id + token).encode('ascii')
            freq_value = pickle.dumps(frequency)
            self.txn.put(combined_key, freq_value, db=self.db_map['tf'])
    
    
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
        # Updates TF related db
        self.__add_tf_map(doc_id, tf_map)
        # Updates IDF related db
        self.__update_nq(doc_id, tf_map.keys())
        # Populate 'token' db using tf_maps
        self.txn.put(doc_id.encode('ascii'), pickle.dumps(tf_map.keys()), db=self.db_map['token'])
        # Update remaining data related to document
        doc_attributes = {
            'file_path': file_path,
            'tags': tags,
            'num_tokens': num_tokens,
            'paragraphs_embeddings': paragraphs_embeddings
        }    
        
        
    def get_doc_list(self) -> list:
        self.__check_requirements()
        doc_list = [ (key, doc_attributes['num_tokens'])
                          for key, doc_attributes in self.txn.cursor(db=self.db_map['doc']) ]
                                                       # .iternext(keys=True, values=False) ]
        return doc_list
    
    
    def get_doc_attributes(self, doc_id: str) -> list:
        self.__check_requirements()
        
        doc_data = self.txn.get(doc_id.encode('ascii'), db=self.db_map['doc'])
        if doc_data is None:
            return None
        
        doc_data = pickle.loads(doc_data)
        
        return doc_data
    
    
    # TO_DO
    def delete_document(self, doc_id: str) -> bool:
        self.__check_requirements()
        
        
    
    def get_tf_token(self, token: str, doc_id: str) -> int:
        self.__check_requirements()
        
        token_id = (token + doc_id).encode('ascii')
        tf_value = self.txn.get(token_id, db=self.db_map['tf'], default=0)
        return int(tf_value)
        
        
    def get_nq_token(self, token: str) -> int:
        self.__check_requirements()
        return self.__get_nq_token(token)
    
    
    def __get_nq_token(self, token: str) -> int:
        nq_value = self.txn.get(token.encode('ascii'), db=self.db_map['nq'], default=0)
        return int(nq_value)