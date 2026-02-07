
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

    file_sections = fields.NestedField(
        properties={
            'file_section_text': fields.TextField(),
            'file_section_embedding': DenseVectorField(dims=768),
        }
    )

    class Index:
        name = 'pdf_files_index'

    class Django:
        model = PDFFile # The Django model
        fields =['id']

    def prepare_file_sections(self, instance):
        # Call the model method to get the data
        return instance.index_pdffile_with_embeddings() 
    
    def prepare_id(self, instance):
        # Call the model method to get the data
        return str(instance.id)

pdf_files_index = Index('pdf_files_index')
pdf_files_index.document(PDFFileDocument)