from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from django.contrib.auth.models import User
from pdffullsearch_backend.models import PDFFile, Category
from pdffullsearch_backend.serializers import UserSerializer, PDFFileSerializer, CategorySerializer
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import os
import ollama
from tika import parser
from langchain_text_splitters import RecursiveCharacterTextSplitter





def index(request):
    client = ollama.Client(host=settings.OLLAMA_API_URL)
    single_embedding = client.embed(
    model='nomic-embed-text',
    input='The quick brown fox jumps over the lazy dog.')
    return HttpResponse(f"Embedding: {single_embedding}")




class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class PDFFileViewSet(viewsets.ModelViewSet):
    serializer_class = PDFFileSerializer
    queryset = PDFFile.objects.all()

class FileUploadView(APIView):
    parser_classes = [FileUploadParser]

    def put(self, request, filename, format=None):
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


    
        return Response(status=204)