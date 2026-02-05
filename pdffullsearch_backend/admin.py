from django.contrib import admin
from pdffullsearch_backend.models import PDFFile, Category

# Register your models here.
admin.site.register(PDFFile)
admin.site.register(Category)