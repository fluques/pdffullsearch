
from operator import index
from django_elasticsearch_dsl.fields import DEDField
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import Document, Nested, Text, Keyword
from django_elasticsearch_dsl import Document, fields
from elasticsearch_dsl import DenseVector as ESDenseVector

import ollama
from langchain_text_splitters import RecursiveCharacterTextSplitter

from pdffullsearch import settings
from pdffullsearch_backend.models import PDFFile
from elasticsearch_dsl  import Index



class DenseVectorField(DEDField, ESDenseVector):
    """
    Custom DenseVectorField for django-elasticsearch-dsl.
    """
    def __init__(self, attr=None, **kwargs):
        # 'dims' is a required parameter for dense_vector fields in Elasticsearch
        if 'dims' not in kwargs:
            raise ValueError("The 'dims' parameter must be specified for DenseVector")
        super().__init__(attr=attr, **kwargs)


    # You may need to override the get_mapping method if not automatically handled
    def get_mapping(self, *args, **kwargs):
        # This returns the specific ES mapping for the field
        return {
            self.name: {
                'type': 'dense_vector',
                'dims': self.dims
            }
        }

@registry.register_document
class PDFFileDocument(Document):
    id = fields.IntegerField(attr='id')
    file_sections = fields.NestedField(
        properties={
            'file_section_text': fields.TextField(),
            'file_section_embedding': DenseVectorField(dims=768),
        }
    )

    def generate_id(self, instance):
        return str(instance.id)

    class Index:
        name = 'pdf_files_index'
        

    class Django:
        model = PDFFile # The Django model
        ignore_signals = True

    '''def prepare_file_sections(self, instance):
        # Call the model method to get the data
        return instance.index_pdffile_with_embeddings() 
    
    def prepare_id(self, instance):
        # Call the model method to get the data
        return str(instance.id)'''

    def index_pdffile_with_embeddings(self, pdf_file_id):
        pdf_file = PDFFile.objects.get(id=pdf_file_id)
        doc = PDFFileDocument()
        doc.meta.id = pdf_file.id
        doc.id = pdf_file.id
        file_sections = []
        # Logic to split content into chunks and generate embeddings
        client = ollama.Client(host=settings.OLLAMA_API_URL)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=settings.OLLAMA_API_MODEL_CHUNK_SIZE,chunk_overlap=settings.OLLAMA_API_MODEL_CHUNK_OVERLAP)
        split_texts = text_splitter.split_text(pdf_file.content)        

        for chunk in split_texts:
            embedding = client.embeddings(model=settings.OLLAMA_API_MODEL, prompt=chunk, options={"num_ctx": settings.OLLAMA_API_MODEL_EMBEDDINGS_DIMENSION} )["embedding"]
            file_sections.append({
                'file_section_text': chunk,
                'file_section_embedding': embedding
            })
        
        doc.file_sections = file_sections
        doc.save()
        pdf_file.embeddings = True
        pdf_file.save(update_fields=['embeddings'])