
from django.contrib.auth.models import User
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from pdffullsearch_backend.models import PDFFile, Category


@registry.register_document
class UserDocument(Document):
    class Index:
        name = "users"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }

    class Django:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
        ]


@registry.register_document
class CategoryDocument(Document):
    id = fields.IntegerField()
    class Index:
        name = "categories"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }

    class Django:
        model = Category
        fields = [
            "name",
            "description",
        ]


@registry.register_document
class PDFFileDocument(Document):
    id = fields.IntegerField()
    categories = fields.ObjectField(properties={
        "id": fields.IntegerField(),
        "name": fields.TextField(),
        "description": fields.TextField(),
    })

    class Index:
        name = "pdf_files"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }

    class Django:
        model = PDFFile
        fields = [
            "path",
            "content",
            "metadata",
            "created_datetime",
            "updated_datetime",
        ]