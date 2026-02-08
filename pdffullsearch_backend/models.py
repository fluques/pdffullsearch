from dataclasses import fields
from django.db import models
from django.conf import settings
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
    embeddings = models.BooleanField(default=False)
    categories = models.ManyToManyField(to=Category, blank=True, related_name="categories")


    class Meta:
        verbose_name_plural = "pdf files"


    def __str__(self):
        return self.name
    

