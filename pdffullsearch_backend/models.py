from dataclasses import fields
from django.db import models
from django.conf import settings
import ollama
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(null=True, blank=True)

    def name_to_string(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return f"{self.name}"
    

class PDFFile(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField()
    metadata = models.TextField()
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)
    file_path = models.CharField(max_length=250)
    categories = models.ManyToManyField(to=Category, blank=True, related_name="categories")

    def index_pdffile_with_embeddings(self):
        #doc = PDFFileDocument() 
        #doc.id = pdffile_instance.id
        file_sections = []
        # Logic to split content into chunks and generate embeddings
        client = ollama.Client(host=settings.OLLAMA_API_URL)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=settings.OLLAMA_API_MODEL_CHUNK_SIZE,chunk_overlap=settings.OLLAMA_API_MODEL_CHUNK_OVERLAP)
        split_texts = text_splitter.split_text(self.content)        

        for chunk in split_texts:
            embedding = client.embeddings(model=settings.OLLAMA_API_MODEL, prompt=chunk, options={"num_ctx": settings.OLLAMA_API_MODEL_EMBEDDINGS_DIMENSION} )["embedding"]
            file_sections.append({
                'file_section_text': chunk,
                'file_section_embedding': embedding
            })
        
        #doc.file_sections = sections_data
        #doc.save()
        return file_sections
    class Meta:
        verbose_name_plural = "pdf files"


    def __str__(self):
        return self.name
    

