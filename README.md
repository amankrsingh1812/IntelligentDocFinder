# Doc-Phi: Intelligent Document Finder

Doc-Phi is a Python based application written for efficient retrieval of documents in your device based on natural language queries. It currently supports the following operations.

- **Adding** documents to Doc-Phi
- **Querying** based on natural language to find the most relevant documents
- **Listing** manually and automatically assigned tags to a particular document

The application consists of a backend daemon service and a command line interface.


## Installation

## Dependencies


## Usage
The command line interface for the doc-phi can be used as:

```
Usage: doc-phi [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  add     Add files to the database
  search  Search files using suitable query
  tags    Retrieve allotted tags for a file
```

Currently following operations can be performed:

### 1. Adding Documents
Various types of the documents can be added using the following syntax:

```
doc-phi add
```

After executing this command, various details pertaining to the document can be added using interactive interface.

### 2. Querying based on Natural Language
Most relevant documents can be queried upon using the following command:

```
doc-phi search -q <query>
```

The results will be displayed in the sorted order based on the rank of the document calculated using [Okapi BM25](https://en.m.wikipedia.org/wiki/Okapi_BM25) ranking function.

### 3. Listing of the Tags
The tags, both manual and automatic, assigned to a document can be viewed using the following command:

```
doc-phi tags -f <file_name>
```
## How Doc-Phi works

The querying backend for Doc-Phi is an amalgamation of conventional ranking algorithm, BM25, based on TF-IDF and contextual sentence level BERT model, MSMARCO. All neural models are implemented on the PyTorch backend. The indexes and documents' metadata is stored using the Lightening Memory-Mapped Database (LMDB). An ontology derived from the union of FIGER and TypeNet ontologies is used by Doc-Phi to automatically assign tags from a generic knowledge space.

The following sections describe the details of various components of the application.

### 1. Document Processing

To be completed...

Include descriptions of the various models/techniques used

### 2. Database Management System
Doc-phi uses **LMDB** (Lightning Memory-Mapped Database) as its database. LMDB is a key-value pair database whose following functionalities motivated its use:

* Read transactions are extremely cheap.  
* Memory mapped, allowing for zero copy lookup and iteration.  
* No application-level caching is required: LMDB fully exploits the operating system’s buffer cache.

More about lmdb can be found at its [official documentation](https://lmdb.readthedocs.io/en/release/#).

#### Schema
![schema](docs/img/uml.jpg)

More about these data stores is as follows:

<ol type='a'>
  <li> <b>document</b><br>
  It contains the details about the documents that are added to the Doc-phi. The documents are identified by a unique identifier <a href="https://docs.python.org/3/library/uuid.html">uuid</a>. The values contain the attribute and its details in the form of dictionary.
  
  <br>
  <li> <b>tf</b><br>
  tf stands for the term-frequency and has its reference from the <a href="https://en.wikipedia.org/wiki/Tf%E2%80%93idf#Term_frequency_2">tf-idf</a>. The tf store contains the frequency of each of the tokens present in all the documents. The key for the tf store is obtained by concatenating the document id with the token itself (as string).

  <br>
  <li> <b>nq</b><br>
  The nq store keeps the track of the documents in which the token has appeared (at least once). It has its significance in the <a href="https://en.m.wikipedia.org/wiki/Okapi_BM25">Okapi BM25</a>. 

  <br>
  <li> <b>token</b><br>
  This data store tracks the list of tokens present in each document. The key is constituted by the document_id. 
</ol>
 

#### Data Access Object (DAO)
Doc-phi utilises DAO as an interface which provides the data operations without exposing the details of the database. As a result, there is no tight coupling between the database and the application logic, and a different database can be used without affecting the main application. 


### 3. Query Processing
Doc-phi takes query in the form of natural language and returns a list of most relevant documents. This entire functionality is handled by the ```QueryEngine``` class and ```SemanticEmbedder``` module. The series of operations can be broken down into following functional unites:

<ol type='a' >
  <li> <b>Non-pipelined processing</b><br>
  The queries are first processed to convert it in the tokens. The process executes in a non-pipelined fashion since the size of queries won't be too large to be executed efficiently by the pipeline. The processing steps are similar to that of the <i>distributed pipeline</i> that we discussed before.

  <br>
  <li> <b>Query Augmentation</b><br>
  The list of tokens retrieved after processing the query undergo an augmentation step. This step improves the search results by adding a variety of semantically similar tokens to the search space of the query. The augmentation process is carried out using the <a href="https://nlpaug.readthedocs.io/en/latest/"> nlapaug </a> module.

  <br>
  <b><li> <b>2-level filtering</b></br></b>
  <ol type='i'>
  <li> <b>Ranking Function</b><br>
  In the 1st level of filtering, <b>Okapi BM25</b> ranking function is used to select top k documents from the search space. Okapi BM25 makes use of the tf-idf on the <i>augmented query tokens</i> to filter out the documents using these query tokens. More details on the ranking function can be found on this <a href="https://en.m.wikipedia.org/wiki/Okapi_BM25"> wikipedia page</a>.

  <br>
  <li> <b>Sentence Embeddings</b><br>
  Sentence embeddings are used to refine and fine-tune the search space by taking into account the semantic meaning of the queries. The ranking function doesn't take into the account the semantic proximity between the tokens and the documents. <br> Sentence embeddings can be calculated using 2 different methods - (i) MSMARCO Models, and (ii) BERT Models. <br>In our implementation, MSMARCO is expected to perform better than the BERT models since MSMARCO directly utilises transformers to calculate the sentence level embeddings. On the other hand for BERT model, first the word embeddings are found out which are then combined to form the sentence embeddings using suitable weights. More details on MSMARCO models can be found <a href="https://www.sbert.net/docs/pretrained-models/msmarco-v3.html"> here</a>. <br>

  On obtaining the sentence embeddings for the query, the cosine similarity is found between the documents obtained after level-1 filtering and the query. Thereafter the resultant documents are displayed in descending order of their relevance.
  </ol>
</ol>

### 4. Command Line Interface

To be completed...

How processes interact

### 5. Miscellaneous

To be completed...

Maybe include other details like design patterns

## License
