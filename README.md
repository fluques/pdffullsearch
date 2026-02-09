# PDFFULLSEARCH

## Description.
Dockerized rest API to index pdf files into elasticsearch database. To search using Ollama embeddings with vectorial index or full text search with inverted index.

## Components
- python
- nginx
- django
- ollama
- elasticsearch
- kafka
- tika
- postgres


## Requirements
1. Docker and compose
    [Docker installation script](https://docs.docker.com/engine/install/ubuntu/)



## Installation
1. Clone the repository:
```bash
git clone https://gitlab.com/pdffullsearch/pdffullsearch.git
```
2. Enter directory:
```bash
cd pdffullsearch
```

3. Run docker-compose file:
```bash
compose -f .\compose.yaml  up --build --force-recreate
```

## Running service on:
```bash
http://127.0.0.1:8989
```


## Curl usage

 ### Upload a pdf file

```bash
curl -XPUT --data-binary "@filename.pdf" http://127.0.0.1:8989/api/pdffile/upload/filename.pdf/
``` 

### Search knn with embeddings
```bash
curl -XGET http://127.0.0.1:8989/api/pdffile/knn_search/ \
  -H "Content-Type: application/json" \
  -d '{"query": "query text", "k": "3", "candidates":"100"}'
```

### Search full text with query text
```bash
curl -XGET http://127.0.0.1:8989/api/pdffile/fulltext_search/ \
  -H "Content-Type: application/json" \
  -d '{"query": "query text"}'
```


## Python usage

 ### Upload a pdf file

```python
import requests
url = 'http://127.0.0.1:8989/api/pdffile/upload/filename.pdf/' 
# Open the file in binary read mode ('rb')
with open('filename.pdf', 'rb') as f:
    files = {'file': f} 
    response = requests.put(url, files=files)
``` 

### Search knn with embeddings
```python
import requests
url = 'http://127.0.0.1:8989/api/pdffile/knn_search/'
payload ={
    'query':'query text',
    'k' : '3',
    'candidates': '100'
}
response = requests.get(url, json=payload)
```

### Search full text with query text
```python
import requests
url = 'http://127.0.0.1:8989/api/pdffile/fulltext_search/' 
payload ={
    'query':'query text'
}
response = requests.get(url, json=payload)
```

