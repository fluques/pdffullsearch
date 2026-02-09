# PDFFULLSEARCH

## Description.
Rest API to index pdf files into elasticsearch database.

## Requirements
1. Docker and compose
    [Docker installation script](https://docs.docker.com/engine/install/ubuntu/)



## Installation
1. Clone the repository:
   ```
    $ git clone https://gitlab.com/pdffullsearch/pdffullsearch.git
   ```

2. Run docker-compose file:
    ```
    $  compose -f .\compose.yaml  up --build --force-recreate
    ```

## Running on service
    ```python
    http://127.0.0.1:8989
    ```

## Endpoint to upload a pdf file
    ```
    http://127.0.0.1:8989/api/pdffile/upload/filename/
    ```

## Endpoint to search knn with embeddings
    ```
    http://127.0.0.1:8989/api/pdffile/knn_search/
    ```

## Endpoint to search full text with query text
    ```
    http://127.0.0.1:8989/api/pdffile/fulltext_search/
    ```
## Usage
