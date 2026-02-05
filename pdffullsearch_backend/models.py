from django.db import models

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
    path = models.CharField(max_length=100)
    content = models.TextField()
    metadata = models.TextField()
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to='documents/')
    categories = models.ManyToManyField(to=Category, blank=True, related_name="categories")

    def path_to_string(self):
        return f"{self.path}"

    class Meta:
        verbose_name_plural = "pdf files"

    def __str__(self):
        return self.path
    
