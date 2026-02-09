# PDFFULLSEARCH

## Description.
Rest API to index pdf files into elasticsearch database.

## Requirements
1. Docker and compose
    [Docker installation script](https://docs.docker.com/engine/install/ubuntu/)



## Installation
1. Clone the repository:
```bash
git clone https://gitlab.com/pdffullsearch/pdffullsearch.git
```

2. Run docker-compose file:
```bash
compose -f .\compose.yaml  up --build --force-recreate
```

## Running on service
```bash
curl -XGET http://127.0.0.1:8989
```


## Usage

 ### Upload a pdf file

```bash
curl -XPUT http://127.0.0.1:8989/api/pdffile/upload/filename/
``` 

### Search knn with embeddings
```bash
$ curl -XGET http://127.0.0.1:8989/api/pdffile/knn_search/
```

### Search full text with query text
```bash
$ curl -XGET http://127.0.0.1:8989/api/pdffile/fulltext_search/
```

