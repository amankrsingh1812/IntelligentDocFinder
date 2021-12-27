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

The results will be displayed in the sorted order based on the rank of the document calculated using **Okapi BM25** ranking function.

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

To be completed...

Include schemas/relations

### 3. Query Processing

To be completed...

### 4. Command Line Interface

To be completed...

How processes interact

### 5. Miscellaneous

To be completed...

Maybe include other details like design patterns

## License
