import asyncio
import json
from asgiref.sync import sync_to_async
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from django.contrib.auth.models import User
from pdffullsearch_backend.models import PDFFile, Category
from pdffullsearch_backend.serializers import UserSerializer, PDFFileSerializer, CategorySerializer
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import os
from tika import parser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pdffullsearch_backend.kafka_client import send_kafka_message
import ollama
from elasticsearch import Elasticsearch

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class PDFFileViewSet(viewsets.ModelViewSet):
    serializer_class = PDFFileSerializer
    queryset = PDFFile.objects.all()

    @action(detail=False, methods=['put'], parser_classes=[FileUploadParser],url_path=r'upload/(?P<filename>[^/]+)')
    def upload(self,request, filename):
        file_obj = request.data['file']
        # Read the file's content into memory (bytes)
        file_obj.seek(0)
        file_content = file_obj.read()

        parsed_data = parser.from_buffer(file_content, serverEndpoint=settings.TIKA_SERVER_ENDPOINT)

        file_path = os.path.join('uploads', file_obj.name)
        saved_path = default_storage.save(file_path, ContentFile(file_content))

        pdf_file = PDFFile.objects.create(
            name=file_obj.name,
            file_path=saved_path,
            content=parsed_data['content'],
            metadata=parsed_data['metadata']
        )
        pdf_file.save()

        # Send Kafka message    
        asyncio.run(send_kafka_message({'id': pdf_file.id}))
        return JsonResponse({"result": "File uploaded successfully", "id": pdf_file.id,"file_path": pdf_file.file_path}, status=200)
    

    @action(detail=False, methods=['get'],url_path=r'knn_search')
    def knn_search(self, request):
        data = json.loads(request.body)
        text_query = data.get('query', None)
        k = data.get('k', 3)
        candidates = data.get('candidates', 100)
        if not text_query:  
            return JsonResponse({"error": "Query parameter is required."}, status=400)
        
        recent = self.search_knn(text_query, k=int(k), candidates=int(candidates))

        return JsonResponse({"count": len(recent), "query": text_query, "search_type": "knn", "results": recent}, status=200)
    

    @action(detail=False, methods=['get'],url_path=r'fulltext_search')
    def fulltext_search(self, request):
        data = json.loads(request.body)
        text_query = data.get('query', None)
        if not text_query:  
            return JsonResponse({"error": "Query parameter is required."}, status=400)
        
        recent = self.search_fulltext(text_query)
        return JsonResponse({"count": len(recent), "query": text_query, "search_type": "fulltext", "results": recent}, status=200)
    


    def get_embeddings(self,text):
        """
        Function to get embeddings for a batch of titles from the OpenAI API.
        """
        client = ollama.Client(host=settings.OLLAMA_API_URL)
        embedding = client.embeddings(model=settings.OLLAMA_API_MODEL, prompt=text)["embedding"]
        return embedding
    
    def search_knn(self, query_text,k=3, candidates=100):
        query_embedding = self.get_embeddings(query_text) # Generate embedding for the query

        knn_query = {
            "_source": ["id", "file_sections.file_section_text"],  # Return the ID and text of the sections
            "knn": {
                "field": "file_sections.file_section_embedding",
                "query_vector": query_embedding,
                "k": k,
                "num_candidates": candidates,
                "boost": 0.5 # Optional: combine with other search methods
            }
        }

        # Execute the search
        es_client = Elasticsearch("http://elasticsearch:9200", request_timeout=120)
        response = es_client.search(index="pdf_files_index", body=knn_query)
        return response['hits']['hits']
    

    def search_fulltext(self, query_text):
        index_name = "pdf_files_index"
        query_body = {
        "_source": ["id", "file_sections.file_section_text"],  # Return the ID and text of the sections
        "query": {
            "nested": {
            "path": "file_sections",
            "query": {
                "bool": {
                "must": [
                    { "match": { "file_sections.file_section_text": query_text} },
                ]
                }
            },
            "score_mode": "max" # Adjust score_mode as needed (avg, sum, max, etc.)
            }
        }
        }
        es_client = Elasticsearch("http://elasticsearch:9200", request_timeout=120)
        response = es_client.search(index=index_name, body=query_body)
        return response["hits"]["hits"]
